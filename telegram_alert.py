import requests
import os

# Try to load .env if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# =========================================
# TELEGRAM CONFIG (from environment)
# =========================================

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================================
# SEND TEXT ALERT
# =========================================

def send_alert():

    message = """
🚨 ACCIDENT DETECTED 🚨

📍 Location: Chennai Main Road
⚠ Severity: HIGH

🚑 Ambulance Alert Sent
👮 Police Alert Sent

CrashSense AI Monitoring System
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message
    }

    try:

        response = requests.post(
            url,
            data=data
        )

        print("✅ Telegram Alert Sent")

        print(response.json())

    except Exception as e:

        print("❌ Telegram Error:", e)

# =========================================
# SEND PHOTO
# =========================================

def send_photo(photo_path):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    try:

        with open(photo_path, "rb") as photo:

            files = {
                "photo": photo
            }

            data = {
                "chat_id": CHAT_ID,
                "caption": "📸 Accident Evidence Captured"
            }

            response = requests.post(
                url,
                files=files,
                data=data
            )

            print("✅ Telegram Photo Sent")

            print(response.json())

    except Exception as e:

        print("❌ Photo Error:", e)

# =========================================
# SEND FULL ALERT
# =========================================

def send_full_alert(photo_path):

    send_alert()

    send_photo(photo_path)