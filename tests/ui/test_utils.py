from pathlib import Path
from datetime import datetime
import requests


BASE_URL = "http://127.0.0.1:8000"


def reset_app_state():
    requests.get(f"{BASE_URL}/reset")


def save_failure_screenshot(page, test_name: str):
    screenshots_dir = Path("reports/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = screenshots_dir / f"{test_name}_{timestamp}.png"

    page.screenshot(path=str(file_path), full_page=True)
    print(f"Screenshot saved: {file_path}")