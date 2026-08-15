import requests

# =========================================
# TELEGRAM CONFIG
# =========================================

BOT_TOKEN = "8654138776:AAEDMeMHRgY1NSuW8pSz4hgPVYJyt1JCNfg"
CHAT_ID = "7410266224"

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