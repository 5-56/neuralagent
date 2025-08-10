import os
import platform
import httpx
import ui_extraction
import mss
from io import BytesIO
from PIL import Image
import base64
import json


def take_screenshot_b64(media_type: str = None, jpeg_quality: int = 80):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        img = img.resize((1280, 720))
        buffer = BytesIO()
        mt = (media_type or os.getenv('NEURALAGENT_SCREENSHOT_MEDIA_TYPE') or 'image/jpeg').lower()
        if mt == 'image/png':
            img.save(buffer, format="PNG")
        else:
            q = int(os.getenv('NEURALAGENT_SCREENSHOT_JPEG_QUALITY') or jpeg_quality or 80)
            img.save(buffer, format="JPEG", quality=max(1, min(95, q)), optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def get_suggestions():
    api_url = os.getenv("NEURALAGENT_API_URL") + '/aiagent/suggestor'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + os.getenv("NEURALAGENT_USER_ACCESS_TOKEN"),
    }

    media_type = os.getenv('NEURALAGENT_SCREENSHOT_MEDIA_TYPE') or 'image/jpeg'

    payload = {
        "current_os": "MacOS" if platform.system() == "darwin" else platform.system(),
        "current_interactive_elements": ui_extraction.extract_interactive_elements(),
        "current_running_apps": ui_extraction.get_running_apps(),
        "screenshot_b64": take_screenshot_b64(media_type=media_type),
        "screenshot_media_type": media_type,
        "override_model_type": os.getenv('NEURALAGENT_OVERRIDE_MODEL_TYPE') or None,
        "override_model_id": os.getenv('NEURALAGENT_OVERRIDE_MODEL_ID') or None,
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post(api_url, json=payload, headers=headers)
            if response.status_code in (200, 201):
                return response.json()
            else:
                return {"suggestions": [], "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"suggestions": [], "error": str(e)}


if __name__ == "__main__":
    suggestions = get_suggestions()
    print(json.dumps(suggestions))
