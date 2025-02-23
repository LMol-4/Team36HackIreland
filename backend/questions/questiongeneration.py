import sys
import os
import tempfile
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from transcription.get_transcription import get_transcription

question_generation = Blueprint("question_generation", __name__)

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

client = OpenAI(api_key=openai_api_key)

QUESTION_PROMPT_TEMPLATE = (
    "Based on the following pitch transcript, generate a numbered list of 10 highly relevant and insightful questions "
    "that experienced investors or a panel of judges might ask the presenter. The questions should critically assess key aspects of the business, focusing on the following dimensions if applicable:\n\n"
    "1. Business Model: Revenue streams, cost structure, and value proposition.\n"
    "2. Scalability: Growth potential, operational constraints, and market demand.\n"
    "3. Market Validation: Customer adoption, traction, and product-market fit.\n"
    "4. Competitive Landscape: Differentiation, barriers to entry, and threats from incumbents.\n"
    "5. Financial Projections: Revenue forecasts, cost assumptions, and funding needs.\n"
    "6. Risk Management: Identifiable risks, contingency plans, and regulatory considerations.\n\n"
    "{transcript}\n\n"
    "Each question should demonstrate a deep understanding of the pitch, critically examine both strengths and potential weaknesses, "
    "and challenge the presenter to substantiate their claims with data, market insights, or strategic foresight. "
    "Format the output as a JSON object with a key 'questions' that contains the list of questions."
)

SYSTEM_MESSAGE = (
    "You are an experienced venture capitalist, skilled at analyzing pitches and asking challenging questions."
)

def generate_questions(transcript: str) -> str:
    """
    Given a pitch transcript, uses the GPT-4o-mini model to generate a JSON-formatted
    numbered list of 10 questions that investors or judges might ask.
    """
    prompt = QUESTION_PROMPT_TEMPLATE.format(transcript=transcript)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
    )

    return completion.choices[0].message

@question_generation.route("/generate-questions", methods=["POST"])
def generate_questions_route():
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video_path = temp_video.name
        video_file.save(video_path)

    try:
        transcript_text = get_transcription(video_path)
    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

    try:
        questions_result = generate_questions(transcript_text)
    except Exception as e:
        return jsonify({"error": f"Error generating questions: {str(e)}"}), 500

    return jsonify({"questions": questions_result}), 200