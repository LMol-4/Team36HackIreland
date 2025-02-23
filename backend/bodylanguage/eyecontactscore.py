import cv2
import os
import sys
import tempfile
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from transcription.get_transcription import get_transcription  # Helper for audio extraction & transcription
from openai import OpenAI

contact_score = Blueprint("contact-score", __name__)

def generate_feedback(transcript: str) -> str:
    """
    Uses the OpenAI API to generate a concise feedback response based on the transcript.
    The response is written in a direct, first-person tone, and it provides a brief summary
    of the pitch along with constructive suggestions. Please keep the feedback under 150 words
    and ensure it doesn't cut off abruptly.
    """
    # Load environment variables from the root directory
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    dotenv_path = os.path.join(root_dir, ".env")
    load_dotenv(dotenv_path)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    client = OpenAI(api_key=openai_api_key)

    prompt = (
        "I have reviewed your pitch transcript. Please provide a concise summary and direct feedback "
        "in a friendly, first-person tone. Your response should include a brief summary of the pitch, "
        "highlight its strengths, and suggest areas for improvement. Keep your response under 150 words, "
        "and ensure it forms a complete, coherent paragraph without cutting off abruptly.\n\n"
        f"Transcript:\n\n{transcript}"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an experienced venture capitalist providing direct feedback on a pitch."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
    )

    summarised_feedback = response.choices[0].message.content.strip()
    return summarised_feedback

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
        frame_skip = 30  # Process every 30th frame
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_skip != 0:
                frame_count += 1
                continue

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

        # Extract the transcript from the video
        transcript_text = get_transcription(temp_video_path)

        # Generate a summarized feedback response based on the transcript
        feedback = generate_feedback(transcript_text)

        # Return both the attention score and the summarized feedback.
        return jsonify({
            "attention_score": avg_attention_score,
            "feedback": feedback
        }), 200
