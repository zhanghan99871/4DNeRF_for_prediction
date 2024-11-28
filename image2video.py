import cv2
import os

# Set the folder containing images
image_folder = "/home/han/Desktop/NeRF/car_test/processed"
# Set the output video file name
output_video = "car_test.mp4"
# Frame rate for the video
fps = 30

# Get a sorted list of image filenames
images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
print(images)

# Read the first image to get the dimensions
first_image_path = os.path.join(image_folder, images[0])
frame = cv2.imread(first_image_path)
height, width, layers = frame.shape

# Define the video codec and create the video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # For MP4
video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# Write images to video
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

video.release()
print(f"Video saved as {output_video}")
