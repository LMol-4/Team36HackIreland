from flask import Blueprint, request, jsonify
import cv2
import os
import uuid

snapshots = Blueprint('snapshots', __name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "frames"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@snapshots.route('/extract-frames', methods=['POST'])
def extract_frames():
    # Check to see that the vide is sent in the payload.
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    interval_seconds = 1 # We can adjust this to whatever amount needed
    
    # Generate a unique filename to avoid conflicts
    file_extension = os.path.splitext(video_file.filename)[-1]
    video_filename = f"{uuid.uuid4()}{file_extension}"
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    video_file.save(video_path)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({"error": "Could not open video file"}), 500
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        cap.release()
        return jsonify({"error": "Invalid FPS, video might be corrupted"}), 500
    
    frame_interval = int(fps * interval_seconds)
    frame_count = 0
    saved_count = 0
    video_frames_folder = os.path.join(OUTPUT_FOLDER, os.path.splitext(video_filename)[0])
    os.makedirs(video_frames_folder, exist_ok=True)
    
    extracted_frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(video_frames_folder, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            extracted_frames.append(frame_filename)
            saved_count += 1
        frame_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    return jsonify({"message": "Frames extracted successfully", "frames": extracted_frames})
