from flask import Blueprint, request, jsonify
import os
import tempfile

transcription = Blueprint("transcription", __name__)


@transcription.route("/transcribe", methods=["POST"])
def transcribe():
    if "video" not in request.files:
        return {"error": "No video file provided"}, 400

    video_file = request.files["video"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video_path = temp_video.name
        video_file.save(video_path)

    try:
        # get transcription
        transcription_text = "example transcription"
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        os.remove(video_path)

    return jsonify({"transcription": transcription_text})
