from flask import Flask, render_template, Response, jsonify
import cv2
import os

from detect import detect_accident

app = Flask(__name__)

# =========================================
# VIDEO PATH
# =========================================

video_path = os.path.join(
    os.path.dirname(__file__),
    'test_video.mp4'
)

# =========================================
# GLOBAL CRASH STATE
# =========================================

crash_state = {
    'detected': False,
    'alert_count': 0
}

# =========================================
# VIDEO STREAM GENERATOR
# =========================================

def generate_frames():

    global crash_state

    camera = cv2.VideoCapture(video_path)

    if not camera.isOpened():

        print(f"Error: Could not open video file at {video_path}")
        return

    print(f"Video loaded successfully: {video_path}")

    frame_count = 0

    while True:

        success, frame = camera.read()

        # Restart video automatically
        if not success:

            print("Restarting video...")

            camera.set(cv2.CAP_PROP_POS_FRAMES, 0)

            continue

        # Resize for better performance
        frame = cv2.resize(frame, (1024, 576))

        # Accident detection
        frame, is_accident = detect_accident(frame)

        # Update state only once
        if is_accident and not crash_state['detected']:

            crash_state['detected'] = True

            crash_state['alert_count'] += 1

            print(
                f"🚨 CRASH DETECTED! "
                f"Alert #{crash_state['alert_count']}"
            )

        # Auto reset after some frames
        if frame_count % 150 == 0:

            crash_state['detected'] = False

        # Encode frame
        ret, buffer = cv2.imencode(
            '.jpg',
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 80]
        )

        if not ret:
            continue

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )

        frame_count += 1

# =========================================
# ROUTES
# =========================================

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/video')
def video():

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route('/api/crash-status')
def crash_status():

    return jsonify(crash_state)

@app.route('/api/reset-alert')
def reset_alert():

    global crash_state

    crash_state['detected'] = False

    return jsonify({
        'status': 'reset',
        'detected': False
    })

# =========================================
# MAIN
# =========================================

if __name__ == "__main__":

    print("🚀 Starting CrashSense AI...")
    print(f"Video Path: {video_path}")
    print(f"Video Exists: {os.path.exists(video_path)}")

    app.run(
        debug=True,
        threaded=True
    )