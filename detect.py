import cv2
import numpy as np
import time
import os

from ultralytics import YOLO

from telegram_alert import send_full_alert

# =========================================
# LOAD YOLO MODEL
# =========================================

model = YOLO("yolov8n.pt")

# Vehicle class IDs
vehicle_classes = [2, 3, 5, 7]

# Alert cooldown
cooldown = 0

# Create screenshots folder
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# =========================================
# IOU CALCULATION
# =========================================

def calculate_iou(box1, box2):

    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    inter_xmin = max(x1_min, x2_min)
    inter_ymin = max(y1_min, y2_min)
    inter_xmax = min(x1_max, x2_max)
    inter_ymax = min(y1_max, y2_max)

    if inter_xmax < inter_xmin or inter_ymax < inter_ymin:
        return 0.0

    inter_area = (
        (inter_xmax - inter_xmin) *
        (inter_ymax - inter_ymin)
    )

    box1_area = (
        (x1_max - x1_min) *
        (y1_max - y1_min)
    )

    box2_area = (
        (x2_max - x2_min) *
        (y2_max - y2_min)
    )

    union_area = (
        box1_area +
        box2_area -
        inter_area
    )

    if union_area == 0:
        return 0.0

    return inter_area / union_area

# =========================================
# COLLISION DETECTION
# =========================================

def is_collision_detected(v1, v2):

    x1_1, y1_1, x2_1, y2_1, c1_x, c1_y, conf1 = v1
    x1_2, y1_2, x2_2, y2_2, c2_x, c2_y, conf2 = v2

    iou = calculate_iou(
        (x1_1, y1_1, x2_1, y2_1),
        (x1_2, y1_2, x2_2, y2_2)
    )

    distance = np.linalg.norm(
        np.array([c1_x, c1_y]) -
        np.array([c2_x, c2_y])
    )

    box1_size = np.sqrt(
        (x2_1 - x1_1) ** 2 +
        (y2_1 - y1_1) ** 2
    )

    box2_size = np.sqrt(
        (x2_2 - x1_2) ** 2 +
        (y2_2 - y1_2) ** 2
    )

    avg_size = (box1_size + box2_size) / 2

    normalized_distance = distance / (avg_size + 1e-5)

    # Better demo thresholds
    iou_threshold = 0.08
    distance_threshold = 1.5

    return (
        (iou > iou_threshold) or
        (
            normalized_distance < distance_threshold
            and iou > 0.03
        )
    )

# =========================================
# MAIN DETECTION FUNCTION
# =========================================

def detect_accident(frame):

    global cooldown

    results = model(frame)

    boxes = results[0].boxes

    vehicles = []

    # =====================================
    # VEHICLE DETECTION
    # =====================================

    for box in boxes:

        cls = int(box.cls[0])

        conf = float(box.conf[0])

        if cls in vehicle_classes and conf > 0.5:

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            vehicles.append(
                (
                    x1, y1,
                    x2, y2,
                    center_x,
                    center_y,
                    conf
                )
            )

            # GREEN BOX
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

    accident_detected = False

    collision_pairs = []

    # =====================================
    # COLLISION CHECK
    # =====================================

    for i in range(len(vehicles)):

        for j in range(i + 1, len(vehicles)):

            v1 = vehicles[i]
            v2 = vehicles[j]

            if is_collision_detected(v1, v2):

                accident_detected = True

                collision_pairs.append((v1, v2))

    # =====================================
    # DRAW COLLISION WARNINGS
    # =====================================

    for v1, v2 in collision_pairs:

        x1_1, y1_1, x2_1, y2_1 = v1[:4]
        x1_2, y1_2, x2_2, y2_2 = v2[:4]

        min_x = min(x1_1, x1_2)
        min_y = min(y1_1, y1_2)

        max_x = max(x2_1, x2_2)
        max_y = max(y2_1, y2_2)

        # RED COLLISION BOX
        cv2.rectangle(
            frame,
            (min_x, min_y),
            (max_x, max_y),
            (0, 0, 255),
            4
        )

        # RED DANGER CIRCLE
        cv2.circle(
            frame,
            (
                (min_x + max_x) // 2,
                (min_y + max_y) // 2
            ),
            20,
            (0, 0, 255),
            -1
        )

    # =====================================
    # ALERT SYSTEM
    # =====================================

    if accident_detected and cooldown == 0:

        cv2.putText(
            frame,
            "ACCIDENT DETECTED!",
            (50, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (0, 0, 255),
            4
        )

        print("🚨 Accident Detected!")

        # Save screenshot
        filename = (
            f"screenshots/"
            f"accident_{int(time.time())}.jpg"
        )

        cv2.imwrite(filename, frame)

        # Telegram alert
        send_full_alert(filename)

        cooldown = 100

    if cooldown > 0:
        cooldown -= 1

    return frame, accident_detected