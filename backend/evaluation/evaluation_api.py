from flask import Blueprint, request, jsonify
from .script_evaluation import get_feedback

evaluation = Blueprint("evaluation", __name__)


@evaluation.route("/evaluate_transcript", methods=["POST"])
def get_feedback():
    if "transcription" not in request.files:
        return {"error": "No transcription provided"}, 400

    try:
        feedback = get_feedback(request.files["transcription"], request.form["pitch_type"])
        return feedback
    except Exception as e:
        return jsonify({"error": str(e)}), 500