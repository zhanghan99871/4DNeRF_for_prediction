import cv2
import os

# Set the video file path
video_path = "/home/han/Desktop/NeRF/ball/ball.mp4"

# Output folder for images
output_folder = "/home/han/Desktop/NeRF/ball/frames"
os.makedirs(output_folder, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    # Save the frame as an image
    if frame_count % 5 == 0:
        frame_filename = os.path.join(output_folder, f"frame_{(frame_count//5):02d}.jpg")
        cv2.imwrite(frame_filename, frame)
    frame_count += 1

cap.release()
print(f"Extracted {frame_count} frames into {output_folder}")
