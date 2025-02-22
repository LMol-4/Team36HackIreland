import cv2
import os

# (cv2 supports multiple video formats)
video_path = "videos/video.mp4" # Gotta adjust to dynamically attain the path (videos/<file_name>) to the specific video
output_folder = "frames" 
interval_seconds = 1  # We can adjust this to make runner.py capture every X amount of seconds

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Verify if the video opened successfully
if not cap.isOpened():
    print(f"Error: Could not open video file {video_path}")
    exit()

# Get FPS and total frame count
fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Ensuring that the FPS is valid to prevent division errors
if fps <= 0:
    print("Error: FPS could not be determined. Video might be corrupted.")
    cap.release()
    exit()

frame_interval = int(fps * interval_seconds)  # Compute interval in frames

frame_count = 0
saved_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        break  # End of video

    # Save frame every X seconds
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_folder, f"frame_{saved_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        saved_count += 1

    frame_count += 1

# Release resources
cap.release()
cv2.destroyAllWindows()