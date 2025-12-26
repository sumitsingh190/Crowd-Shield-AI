import cv2
import time
import threading
import numpy as np
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

router = APIRouter()

latest_frame = None
frame_lock = threading.Lock()

# ==============================
# RECEIVE FRAME FROM ML
# ==============================
@router.post("/frame")
async def receive_frame(frame: UploadFile = File(...)):
    global latest_frame
    data = await frame.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    with frame_lock:
        latest_frame = img

    return {"ok": True}

# ==============================
# STREAM FRAME TO FRONTEND
# ==============================
def generate_frames():
    global latest_frame
    while True:
        with frame_lock:
            if latest_frame is None:
                continue
            frame = latest_frame.copy()

        _, buffer = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )
        time.sleep(1 / 20)  # ML-paced FPS

@router.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
