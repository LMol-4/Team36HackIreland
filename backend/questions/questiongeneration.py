import sys
import os
import tempfile
import json
import re
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
from transcription.get_transcription import get_transcription  # Helper for audio extraction & transcription

question_generation = Blueprint("question_generation", __name__)

def extract_json_from_markdown(markdown_str: str) -> dict:
    """
    Extracts JSON content from a markdown code block.
    It looks for content wrapped between ```json and ``` markers.
    """
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, markdown_str, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        # If not found, assume the entire string is JSON.
        json_str = markdown_str.strip()

    try:
        return json.loads(json_str)
    except Exception as e:
        print("Error parsing JSON from markdown:", e)
        print("Attempted JSON string:", json_str)
        return None


def generate_questions(transcript: str) -> str:
    """
    Given a pitch transcript, uses the GPT-4o model to generate a JSON-formatted
    numbered list of 10 questions that investors or judges might ask.
    """
    # Load the .env file from the root directory (one level up)
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    dotenv_path = os.path.join(root_dir, ".env")
    load_dotenv(dotenv_path)

    # Retrieve the OpenAI API key from the .env file
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=openai_api_key)

    prompt = (
        "Based on the following pitch transcript, generate a numbered list of 10 highly relevant and insightful questions "
        "that experienced investors or a panel of judges might ask the presenter. The questions should critically assess key aspects of the business, focusing on the following dimensions if applicable:\n\n"
        "1. Business Model: Revenue streams, cost structure, and value proposition.\n"
        "2. Scalability: Growth potential, operational constraints, and market demand.\n"
        "3. Market Validation: Customer adoption, traction, and product-market fit.\n"
        "4. Competitive Landscape: Differentiation, barriers to entry, and threats from incumbents.\n"
        "5. Financial Projections: Revenue forecasts, cost assumptions, and funding needs.\n"
        "6. Risk Management: Identifiable risks, contingency plans, and regulatory considerations.\n\n"
        f"{transcript}\n\n"
        "Each question should demonstrate a deep understanding of the pitch, critically examine both strengths and potential weaknesses, "
        "and challenge the presenter to substantiate their claims with data, market insights, or strategic foresight. "
        "Format the output as a JSON object with a key 'questions' that contains the list of questions."
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced venture capitalist, skilled at analyzing pitches and asking challenging questions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=2000,
    )

    # Return the ChatCompletionMessage object as a string
    return completion.choices[0].message.content

@question_generation.route("/generate-questions", methods=["POST"])
def generate_questions_route():
    # Check that a video file is provided
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files["video"]

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        video_path = temp_video.name
        video_file.save(video_path)

    try:
        # Extract transcript from the video using your helper function
        transcript_text = get_transcription(video_path)
    except Exception as e:
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({"error": str(e)}), 500
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

    try:
        # Generate questions based on the transcript
        questions_result = generate_questions(transcript_text)
        # Extract and parse the JSON from the markdown formatted response
        questions_json = extract_json_from_markdown(questions_result)
        if questions_json is None:
            return jsonify({"error": "Failed to parse questions JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"Error generating questions: {str(e)}"}), 500

    # Return the generated questions as JSON
    return jsonify(questions_json), 200
