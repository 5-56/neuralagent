from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlmodel import Session, select, and_
from db.database import get_session
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from utils import constants
from botocore.config import Config
from langchain_aws import ChatBedrockConverse
from langchain_openai import AzureChatOpenAI
import json
from utils import ai_prompts
from utils.procedures import CustomError, extract_json, extract_json_array
from dependencies.auth_dependencies import get_current_user_dependency
from db.models import (User, Thread, ThreadStatus, ThreadTask, ThreadTaskStatus, ThreadMessage,
                       ThreadChatType, ThreadChatFromChoices, ThreadTaskPlan, ThreadTaskPlanStatus,
                       PlanSubtask, SubtaskStatus, ThreadTaskMemoryEntry, SubtaskType)
from schemas.aiagent import NextStepRequest, CurrentSubtaskRequestObj
from utils.agentic_tools import run_tool_server_side
from utils import llm_provider
from base64 import b64decode
import io
import os
from utils import upload_helper


router = APIRouter(
    prefix='/aiagent',
    tags=['aiagent'],
    dependencies=[Depends(get_current_user_dependency)]
)


@router.post('/{tid}/current_subtask')
def current_subtask_request(tid: str, current_subtask_request_obj: CurrentSubtaskRequestObj,
                            db: Session = Depends(get_session), user: User = Depends(get_current_user_dependency)):
    instance = db.exec(select(Thread).where(and_(
        Thread.id == tid,
        Thread.user_id == user.id,
        Thread.status == ThreadStatus.WORKING
    ))).first()

    if not instance:
        raise CustomError(status.HTTP_404_NOT_FOUND, 'Thread not found')

    task = db.exec(select(ThreadTask).where(and_(
        ThreadTask.thread_id == tid,
        ThreadTask.status == ThreadTaskStatus.WORKING,
    ))).first()

    if not task:
        raise CustomError(status.HTTP_404_NOT_FOUND, 'Thread has no running task')

    current_plan = db.exec(select(ThreadTaskPlan).where(and_(
        ThreadTaskPlan.thread_task_id == task.id,
        ThreadTaskPlan.status == ThreadTaskPlanStatus.ACTIVE,
    ))).first()

    if not current_plan:
        previous_tasks = db.exec(select(ThreadTask).where(and_(
            ThreadTask.thread.has(Thread.user_id == user.id),
            ThreadTask.thread.has(Thread.status != ThreadStatus.DELETED),
            ThreadTask.status != ThreadTaskStatus.WORKING,
        )).order_by(ThreadTask.created_at.desc()).limit(10)).all()
        previous_tasks_arr = []
        for previous_task in previous_tasks:
            previous_tasks_arr.append({
                'task': previous_task.task_text,
                'status': previous_task.status,
            })

        # Allow override for planner model
        if current_subtask_request_obj.override_planner_model_type and current_subtask_request_obj.override_planner_model_id:
            llm = llm_provider.get_llm_override(
                model_type=current_subtask_request_obj.override_planner_model_type,
                model_id=current_subtask_request_obj.override_planner_model_id,
                temperature=0.3,
            )
        else:
            llm = llm_provider.get_llm(agent='planner', temperature=0.3)

        plan_user_message = [
            {
                'type': 'text',
                'text': f'Current OS: {current_subtask_request_obj.current_os} \n\nCurrent Visible OS Native Interactive Elements: {json.dumps(current_subtask_request_obj.current_interactive_elements)}'
            },
            {
                'type': 'text',
                'text': f'Current Running Apps: {json.dumps(current_subtask_request_obj.current_running_apps)}'
            }
        ]

        if len(previous_tasks_arr) > 0:
            plan_user_message.append({
                'type': 'text',
                'text': f'Previous Tasks (Limited to 10): \n {json.dumps(previous_tasks_arr)}',
            })

        plan_user_message.append({
            'type': 'text',
            'text': f'Task: {task.task_text}'
        })

        plan_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(ai_prompts.PLANNER_AGENT_PROMPT),
            HumanMessage(content=plan_user_message),
        ])

        chain = plan_prompt | llm
        plan_response = chain.invoke({})
        plan_response_data = extract_json(plan_response.content)

        plan = plan_response_data.get('subtasks')

        plan_ai_message = ThreadMessage(
            thread_id=instance.id,
            thread_chat_type=ThreadChatType.PLAN,
            thread_chat_from=ThreadChatFromChoices.FROM_AI,
            text=json.dumps(plan_response_data),
        )
        db.add(plan_ai_message)
        db.commit()
        db.refresh(plan_ai_message)

        current_plan = ThreadTaskPlan(
            thread_task_id=task.id,
        )
        db.add(current_plan)
        db.commit()
        db.refresh(current_plan)

        for i, subtask_item in enumerate(plan):
            subtask = PlanSubtask(
                thread_task_plan_id=current_plan.id,
                subtask_text=subtask_item.get('subtask'),
                subtask_type=SubtaskType.DESKTOP,
                ordering=i + 1,
            )
            db.add(subtask)
            db.commit()
            db.refresh(subtask)

        if len(plan) == 0:
            ai_message = ThreadMessage(
                thread_id=instance.id,
                thread_task_id=task.id,
                thread_chat_type=ThreadChatType.DESKTOP_USE,
                thread_chat_from=ThreadChatFromChoices.FROM_AI,
                text=json.dumps({'actions': [{'action': 'task_completed'}]}),
            )
            db.add(ai_message)
            db.commit()
            db.refresh(ai_message)

            return {'action': 'task_completed'}

    current_subtask = db.exec(select(PlanSubtask).where(and_(
        PlanSubtask.status == SubtaskStatus.ACTIVE,
        PlanSubtask.thread_task_plan_id == current_plan.id
    )).order_by(PlanSubtask.ordering.asc())).first()

    if not current_subtask:
        current_plan.status = ThreadTaskPlanStatus.COMPLETED
        db.add(current_plan)
        db.commit()
        db.refresh(current_plan)

        task.status = ThreadTaskStatus.COMPLETED
        db.add(task)
        db.commit()
        db.refresh(task)

        instance.status = ThreadStatus.STANDBY
        db.add(instance)
        db.commit()
        db.refresh(instance)

        ai_message = ThreadMessage(
            thread_id=instance.id,
            thread_task_id=task.id,
            thread_chat_type=ThreadChatType.DESKTOP_USE,
            thread_chat_from=ThreadChatFromChoices.FROM_AI,
            text=json.dumps({'actions': [{'action': 'task_completed'}]}),
        )
        db.add(ai_message)
        db.commit()
        db.refresh(ai_message)

        return {'action': 'task_completed'}

    return {
        'id': current_subtask.id,
        'subtask_text': current_subtask.subtask_text,
        'subtask_type': current_subtask.subtask_type,
        'status': current_subtask.status,
    }


@router.post('/{tid}/next_step')
def next_step(tid: str, next_step_req: NextStepRequest, db: Session = Depends(get_session),
              user: User = Depends(get_current_user_dependency)):
    instance = db.exec(select(Thread).where(and_(
        Thread.id == tid,
        Thread.user_id == user.id,
        Thread.status == ThreadStatus.WORKING
    ))).first()

    if not instance:
        raise CustomError(status.HTTP_404_NOT_FOUND, 'Thread not found')

    task = db.exec(select(ThreadTask).where(and_(
        ThreadTask.thread_id == tid,
        ThreadTask.status == ThreadTaskStatus.WORKING,
    ))).first()

    if not task:
        raise CustomError(status.HTTP_404_NOT_FOUND, 'Thread has no running task')

    current_plan = db.exec(select(ThreadTaskPlan).where(and_(
        ThreadTaskPlan.thread_task_id == task.id,
        ThreadTaskPlan.status == ThreadTaskPlanStatus.ACTIVE,
    ))).first()

    current_subtask = db.exec(select(PlanSubtask).where(and_(
        PlanSubtask.status == SubtaskStatus.ACTIVE,
        PlanSubtask.thread_task_plan_id == current_plan.id
    )).order_by(PlanSubtask.ordering.asc())).first()
    if not current_subtask or current_subtask.subtask_type != SubtaskType.DESKTOP:
        raise CustomError(status.HTTP_404_NOT_FOUND, 'No Current Desktop Task!')

    # Allow per-request override for computer_use model
    if next_step_req.override_model_type and next_step_req.override_model_id:
        llm = llm_provider.get_llm_override(
            model_type=next_step_req.override_model_type,
            model_id=next_step_req.override_model_id,
            temperature=1.0 if task.extended_thinking_mode else 0.0,
            thinking_enabled=task.extended_thinking_mode,
        )
    else:
        if task.extended_thinking_mode is True:
            llm = llm_provider.get_llm(agent='computer_use', temperature=1.0, thinking_enabled=True)
        else:
            llm = llm_provider.get_llm(agent='computer_use', temperature=0.0)

    previous_subtasks = db.exec(select(PlanSubtask).where(and_(
        PlanSubtask.status != SubtaskStatus.ACTIVE,
        PlanSubtask.plan.has(ThreadTaskPlan.thread_task_id == task.id)
    )).order_by(PlanSubtask.ordering.asc())).all()
    previous_subtasks_arr = []
    for previous_subtask in previous_subtasks:
        previous_subtasks_arr.append({
            'subtask_text': previous_subtask.subtask_text,
            'status': previous_subtask.status,
        })

    screenshot_user_message_block = None
    screenshot_s3_path = None
    if next_step_req.screenshot_b64:
        if os.getenv('ENABLE_SCREENSHOT_LOGGING_FOR_TRAINING') == 'true':
            image_bytes = b64decode(next_step_req.screenshot_b64)
            image_io = io.BytesIO(image_bytes)
            screenshot_s3_path = upload_helper.upload_screenshot_s3_bytesio(image_io, extension="png")
        
        # Respect requested media type for providers which require image_url vs base64
        if os.getenv('COMPUTER_USE_AGENT_MODEL_TYPE') == 'ollama' or (next_step_req.screenshot_media_type and next_step_req.screenshot_media_type.startswith('image_url')):
            screenshot_user_message_block = {
                "type": "image_url",
                "image_url": f"data:{next_step_req.screenshot_media_type or 'image/png'};base64,{next_step_req.screenshot_b64}"
            }
        else:
            screenshot_user_message_block = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": next_step_req.screenshot_media_type or "image/png",
                    "data": next_step_req.screenshot_b64
                }
            }

    action_history = []
    task_previous_messages = db.exec(
        select(ThreadMessage)
        .where(
            and_(
                ThreadMessage.thread_task_id == task.id,
                ThreadMessage.thread_chat_type == ThreadChatType.DESKTOP_USE,
            )
        )
        .order_by(ThreadMessage.created_at.desc())
        .limit(5)
    ).all()
    for m in task_previous_messages:
        try:
            payload = json.loads(m.text)
            action_history.append(payload)
        except Exception:
            pass

    prompt_data = ai_prompts.COMPUTER_USE_SYSTEM_PROMPT

    user_message_block = [
        {
            'type': 'text',
            'text': f'Current OS: {next_step_req.current_os}'
        },
        {
            'type': 'text',
            'text': f'Current Visible OS Native Interactive Elements: {json.dumps(next_step_req.current_interactive_elements)}'
        },
        {
            'type': 'text',
            'text': f'Current Running Apps: {json.dumps(next_step_req.current_running_apps)}'
        },
    ]

    if len(previous_subtasks_arr) > 0:
        user_message_block.append({
            'type': 'text',
            'text': f'Previous Subtasks (Limited to 10): \n {json.dumps(previous_subtasks_arr)}',
        })

    if screenshot_user_message_block is not None:
        user_message_block.append(screenshot_user_message_block)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(prompt_data),
        HumanMessage(content=user_message_block)
    ])

    chain = prompt | llm
    response = chain.invoke({})
    response_data = extract_json(response.content)

    ai_message = ThreadMessage(
        thread_id=instance.id,
        thread_task_id=task.id,
        thread_chat_type=ThreadChatType.DESKTOP_USE,
        thread_chat_from=ThreadChatFromChoices.FROM_AI,
        text=json.dumps(response_data),
        screenshot=screenshot_s3_path
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)

    return response_data
