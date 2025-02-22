import cv2
import os
import tempfile
import shutil
import sys

def calculate_average_attention_score(video_path):
    """
    Processes the given video file at video_path, calculates the average attention score,
    and deletes the temporary file after processing.

    Args:
        video_path (str): Path to the video file.

    Returns:
        float: The average attention score.
    """
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return 0.0

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_video_path = os.path.join(temp_dir, os.path.basename(video_path))
        shutil.copy2(video_path, temp_video_path)

        # Initialize video capture with the temporary video file
        cap = cv2.VideoCapture(temp_video_path)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return 0.0

        # Load pre-trained Haar cascades for face and eye detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        attention_scores = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            attention_score = 0

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                # Detect eyes within the face region
                eyes = eye_cascade.detectMultiScale(roi_gray)
                if len(eyes) >= 2:
                    attention_score = 100  # Both eyes detected, assuming full attention
                else:
                    attention_score = 50   # Less than two eyes detected, partial attention

            attention_scores.append(attention_score)

        cap.release()

        # Return the score by calculating average
        if attention_scores:
            return sum(attention_scores) / len(attention_scores)
        else:
            print("No attention scores to average.")
            return 0.0

def main():
    if len(sys.argv) < 2:
        print("Usage: python your_script.py /path/to/video.mp4")
        sys.exit(1)

    video_path = sys.argv[1]
    average_attention = calculate_average_attention_score(video_path)
    print(f'Average Attention Score: {average_attention:.2f}')

if __name__ == '__main__':
    main()
