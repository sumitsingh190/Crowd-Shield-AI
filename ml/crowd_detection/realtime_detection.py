from ultralytics import YOLO
import cv2
import numpy as np
import requests
import time
from collections import deque

# ==============================
# CONFIG
# ==============================
VIDEO_PATH = "data/videos/crowd.mp4"
BACKEND_INGEST = "http://127.0.0.1:8000/ingest"
BACKEND_FRAME = "http://127.0.0.1:8000/frame"

TARGET_FPS = 20
FRAME_SKIP = 2
SEND_INTERVAL = 1.0
GRID_SIZE = 5

CONF_THRESHOLD = 0.35
MAX_DENSITY_CAP = 6

# ==============================
# INIT
# ==============================
model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(VIDEO_PATH)

frame_delay = int(1000 / TARGET_FPS)
last_sent_time = 0
frame_id = 0

count_history = deque(maxlen=10)

print("▶️ CrowdShield AI ML Pipeline Started")

# ==============================
# RESET BACKEND
# ==============================
try:
    requests.post(BACKEND_INGEST, json={"reset": True}, timeout=2)
    print("♻ Backend reset")
except:
    pass

# ==============================
# MAIN LOOP
# ==============================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    if frame_id % FRAME_SKIP != 0:
        cv2.waitKey(frame_delay)
        continue

    h, w, _ = frame.shape
    resized = cv2.resize(frame, (640, int(640 * h / w)))

    # ==============================
    # YOLO
    # ==============================
    results = model.predict(
        resized,
        imgsz=640,
        conf=CONF_THRESHOLD,
        classes=[0],
        verbose=False
    )

    zone_counts = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.int32)
    visible_count = 0

    for r in results:
        if r.boxes is None:
            continue
        boxes = r.boxes.xyxy.cpu().numpy()
        for box in boxes:
            visible_count += 1
            x1, y1, x2, y2 = (box * (w / 640)).astype(int)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            zx = min(int(cx / w * GRID_SIZE), GRID_SIZE - 1)
            zy = min(int(cy / h * GRID_SIZE), GRID_SIZE - 1)
            zone_counts[zy][zx] += 1
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    count_history.append(visible_count)
    crowd_count = int(np.mean(count_history))

    avg_density = float(zone_counts.mean())
    max_density = int(zone_counts.max())

    density_score = min(max_density / MAX_DENSITY_CAP, 1.0)

    if density_score < 0.3:
        status, color = "SAFE", (0, 200, 0)
    elif density_score < 0.6:
        status, color = "WARNING", (0, 255, 255)
    else:
        status, color = "CRITICAL", (0, 0, 255)

    # ==============================
    # OVERLAY
    # ==============================
    cv2.rectangle(frame, (0, 0), (520, 120), color, -1)
    cv2.putText(frame, f"People: {crowd_count}", (15, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(frame, f"Max Density: {max_density}", (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    cv2.putText(frame, f"Status: {status}", (15, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # ==============================
    # SEND DATA + FRAME
    # ==============================
    now = time.time()
    if now - last_sent_time >= SEND_INTERVAL:
        try:
            requests.post(BACKEND_INGEST, json={
                "crowd_count": crowd_count,
                "avg_density": avg_density,
                "max_density": max_density,
                "risk_score": round(density_score * 100, 2),
                "status": status
            }, timeout=0.3)

            _, jpeg = cv2.imencode(".jpg", frame)
            requests.post(BACKEND_FRAME,
                          files={"frame": jpeg.tobytes()},
                          timeout=0.3)
        except:
            pass

        last_sent_time = now

    cv2.imshow("CrowdShield AI", frame)
    if cv2.waitKey(frame_delay) & 0xFF == ord("q"):
        break

# ==============================
# FINISH
# ==============================
requests.post(BACKEND_INGEST, json={"completed": True})
cap.release()
cv2.destroyAllWindows()
print("🏁 ML Video Completed")
