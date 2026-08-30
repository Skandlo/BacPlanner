import json
from pathlib import Path

# تحديد مسار ملف الإعدادات بجانب التطبيق
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"

def load_api_key():
    """Loads the API key from the local config file if it exists."""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("gemini_api_key")
        except Exception:
            return None
    return None

def save_api_key(api_key):
    """Saves the API key securely to the local config file."""
    try:
        data = {"gemini_api_key": api_key.strip()}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return false