from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class NextStepRequest(BaseModel):
    screenshot_b64: Optional[str] = None
    current_interactive_elements: list[dict] = []
    current_os: str
    current_running_apps: list[dict] = []
    # Optional overrides for model selection (computer_use agent)
    override_model_type: Optional[str] = None
    override_model_id: Optional[str] = None
    # Optional screenshot media type, defaults to image/png if not provided
    screenshot_media_type: Optional[str] = None


class BackgroundNextStepRequest(BaseModel):
    screenshot_b64: Optional[str] = None
    current_open_tabs: list[dict] = []
    current_url: str


class CurrentSubtaskRequestObj(BaseModel):
    current_interactive_elements: list[dict] = []
    current_os: str
    current_running_apps: list[dict] = []
    # Optional overrides for model selection (planner agent)
    override_planner_model_type: Optional[str] = None
    override_planner_model_id: Optional[str] = None


class SuggestorRequest(BaseModel):
    current_interactive_elements: list[dict] = []
    current_os: str
    current_running_apps: list[dict] = []
    screenshot_b64: Optional[str] = None
