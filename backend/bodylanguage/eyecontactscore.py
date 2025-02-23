import cv2
import os
import tempfile
from flask import Blueprint, request, jsonify

contact_score = Blueprint("contact-score", __name__)

@contact_score.route("", methods=["POST"])
def calculate_average_attention_score():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]
    if video_file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_video_path = os.path.join(temp_dir, video_file.filename)
        video_file.save(temp_video_path)

        cap = cv2.VideoCapture(temp_video_path)
        if not cap.isOpened():
            return jsonify({"error": "Unable to open video file"}), 500

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        attention_scores = []
        frame_skip = 30  # Process every 30th frame (adjust based on video FPS and desired sampling rate)
        frame_count = 0

        print(f'Reached here!')
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Skip frames to reduce processing load
            if frame_count % frame_skip != 0:
                frame_count += 1
                continue

            # Optionally resize the frame for faster processing
            frame = cv2.resize(frame, (640, 480))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            attention_score = 0

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) >= 2:
                    attention_score = 100  # Full attention
                else:
                    attention_score = 50   # Partial attention

            attention_scores.append(attention_score)
            frame_count += 1

        cap.release()

        if attention_scores:
            avg_attention_score = sum(attention_scores) / len(attention_scores)
        else:
            avg_attention_score = 0.0

        return jsonify({"attention_score": avg_attention_score}), 200
