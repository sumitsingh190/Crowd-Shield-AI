import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt

# Load model
model = hub.load("https://tfhub.dev/tensorflow/efficientdet/lite2/detection/1")

# Load image
image_path = "data/frames/frame_0.jpg"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

h, w, _ = image.shape

# Prepare input
input_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.uint8)
input_tensor = input_tensor[tf.newaxis, ...]

# Run detection
outputs = model(input_tensor)
boxes = outputs["detection_boxes"][0].numpy()
classes = outputs["detection_classes"][0].numpy().astype(int)
scores = outputs["detection_scores"][0].numpy()

# Grid size
GRID_SIZE = 5
density_grid = np.zeros((GRID_SIZE, GRID_SIZE))

# Populate density grid
for box, cls, score in zip(boxes, classes, scores):
    if cls == 1 and score > 0.5:  # person
        y1, x1, y2, x2 = box
        cx = int(((x1 + x2) / 2) * w)
        cy = int(((y1 + y2) / 2) * h)

        grid_x = min(cx * GRID_SIZE // w, GRID_SIZE - 1)
        grid_y = min(cy * GRID_SIZE // h, GRID_SIZE - 1)

        density_grid[grid_y][grid_x] += 1

print("Density Grid:\n", density_grid)

# Plot heatmap
plt.figure(figsize=(6, 5))
plt.imshow(density_grid, cmap="hot")
plt.colorbar(label="People Count")
plt.title("Crowd Density Heatmap")
plt.xlabel("X Zone")
plt.ylabel("Y Zone")
plt.show()
