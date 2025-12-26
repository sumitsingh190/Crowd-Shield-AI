import cv2
import os

video_path = "data/videos/crowd.mp4"
output_dir = "data/frames"

os.makedirs(output_dir, exist_ok=True)

cap = cv2.VideoCapture(video_path)
frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imwrite(f"{output_dir}/frame_{frame_id}.jpg", frame)
    frame_id += 1

cap.release()
print(f"Extracted {frame_id} frames")
