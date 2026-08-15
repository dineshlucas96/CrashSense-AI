🚨 CrashSense AI

Real-Time Road Accident Detection & Alert System

CrashSense AI is an intelligent computer-vision system designed to detect vehicle collisions from video feeds in real time. It uses YOLOv8, OpenCV, and custom IoU + normalized-distance collision logic to identify potential crashes and automatically send alerts through the Telegram Bot API.

The project also includes a Flask-based web dashboard that provides live annotated video streaming, crash-status monitoring, and an alert counter.

Built as an AI & Data Science project using Python, YOLOv8, OpenCV, Flask, and Telegram Bot API.

✨ Key Features

🚗 Real-time vehicle detection using YOLOv8n

💥 Collision detection using IoU and normalized-distance checks

📹 Live MJPEG video streaming through a browser

🟢 Green bounding boxes for detected vehicles

🔴 Red bounding boxes and collision markers for detected crash zones

📸 Automatic screenshot capture when a collision is detected

📲 Instant Telegram text + image alerts

⏱️ 100-frame alert cooldown to reduce duplicate notifications

🔄 Automatic video restart when playback ends

🌐 Crash-status REST API

📊 Session-based accident alert counter

🌑 Responsive glassmorphism dark-themed dashboard

🧠 How It Works

Video / CCTV Feed
       ↓
   OpenCV Capture
       ↓
    YOLOv8n
       ↓
Vehicle Detection
       ↓
IoU + Distance Collision Logic
       ↓
   Crash Detected?
      ↙       ↘
    No         Yes
                ↓
       Save Screenshot
                ↓
        Telegram Alert
                ↓
       Web Dashboard

🔍 Detection Methodology

1. Vehicle Detection

CrashSense AI uses the YOLOv8n (nano) model for real-time object detection.

The system considers these vehicle classes:

Car — COCO class 2

Motorcycle — COCO class 3

Bus — COCO class 5

Truck — COCO class 7

Only detections with confidence greater than 0.50 are considered valid.

2. Collision Detection

For every unique pair of detected vehicles, the system evaluates:

Intersection over Union (IoU)

A collision can be flagged when vehicle bounding boxes overlap beyond the configured threshold.

Normalized Center Distance

The center-to-center distance between two vehicles is normalized using their average bounding-box diagonal.

The current collision logic uses:

IoU > 0.08 → collision flag

Normalized distance < 1.5 and IoU > 0.03 → collision flag

When a collision is confirmed:

A red bounding region is drawn around the vehicles.

A red circle marks the collision centroid.

A screenshot is saved.

A Telegram notification is sent.

📲 Telegram Alert Pipeline

When the first collision in an event is detected:

The annotated frame is saved as a JPEG.

A timestamp-based filename is generated.

A Telegram text alert is sent.

The accident screenshot is sent as evidence.

A cooldown prevents repeated alerts for the same event.

Keep your Telegram bot token and chat ID private. Do not commit them to GitHub.

🌐 Web Dashboard

The Flask application provides:

Route

Purpose

/

Main dashboard

/video

Live MJPEG video stream

/api/crash-status

JSON crash-status API

The frontend polls the crash-status endpoint every 500 ms to update the live status, alert badge, and session alert counter.

🛠️ Technology Stack

Technology

Purpose

Python 3.9+

Core programming language

YOLOv8n / Ultralytics

Vehicle detection

OpenCV

Video processing and annotation

Flask

Web server and API

NumPy

Numerical calculations

Telegram Bot API

Emergency alerts

HTML/CSS/JavaScript

Dashboard interface

📁 Project Structure

CrashSense-AI/
│
├── app.py
├── detect.py
├── telegram_alert.py
├── requirements.txt
├── yolov8n.pt
├── test_video.mp4
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── screenshots/
    └── accident_*.jpg

File Description

app.py — Flask server, video streaming, and crash-state management

detect.py — YOLOv8 inference, collision logic, annotations, and screenshot saving

telegram_alert.py — Telegram text and photo alert functions

templates/index.html — Web dashboard

static/style.css — Dashboard styling and animations

yolov8n.pt — YOLOv8 nano model weights

test_video.mp4 — Sample road footage for testing

screenshots/ — Accident evidence images generated during detection

⚙️ Installation

1. Clone the repository

git clone https://github.com/YOUR-USERNAME/CrashSense-AI.git
cd CrashSense-AI

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

On Linux/macOS:

source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure Telegram

Create a Telegram bot using BotFather and obtain:

Bot Token

Chat ID

Configure them using environment variables or your project's configuration method.

Never hard-code or upload your bot token to GitHub.

Example:

TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

5. Run the application

python app.py

Open the local Flask URL shown in the terminal, typically:

http://127.0.0.1:5000

🎥 Using Your Own Video

You can test the system using a local MP4 road video or adapt the OpenCV VideoCapture source for a CCTV/RTSP stream.

For example:

cv2.VideoCapture("test_video.mp4")

or for a camera:

cv2.VideoCapture(0)

For RTSP/CCTV integration, configure the appropriate stream URL in the application.

📊 Results & Observations

Testing described in the project report showed:

Vehicle detection: approximately 85–90% under standard road conditions with YOLOv8n

Telegram alert latency: approximately 1–2 seconds after detection

Video streaming: 1024×576 MJPEG browser stream

False-positive mitigation: 100-frame cooldown helps reduce duplicate notifications

These results are dependent on video quality, camera angle, lighting, vehicle density, and hardware.

🚀 Future Scope

Planned improvements include:

📍 GPS tagging for exact accident coordinates

📹 Multi-camera monitoring

🧠 Accident severity classification

📡 Live CCTV/RTSP integration

📱 Android/iOS first-responder application

🗄️ Accident database and analytics

⚡ Edge deployment on Jetson Nano or Raspberry Pi

⚠️ Limitations

CrashSense AI is a prototype/research project and should not be treated as a certified emergency-response system.

Collision detection performance can vary depending on:

Camera position

Lighting conditions

Video resolution

Occlusion

Traffic density

Vehicle overlap

Model confidence

Human verification and integration with appropriate emergency infrastructure would be required for real-world deployment.

🎯 Project Objective

The goal of CrashSense AI is to demonstrate how deep learning + computer vision + automated communication can be combined into an end-to-end road safety system.

Instead of relying entirely on continuous human CCTV monitoring, the system attempts to identify collision events automatically and provide immediate visual evidence through Telegram alerts.

👨‍💻 Author

DineshKumar S
B.Tech Artificial Intelligence & Data Science
New Prince Shri Bhavani College of Engineering and Technology

📄 Project Report

The project report contains the detailed methodology, architecture, technology stack, observations, and future scope.

⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub!
