from flask import Blueprint, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
import sys

answer_feedback = Blueprint("answer-feedback", __name__)

def judge_response(question: str, answer: str) -> str:
    """
    Given a single question and its corresponding answer, this function constructs
    a prompt to have the OpenAI API evaluate the response. It returns the evaluator's feedback
    as a plain text string.
    """
    prompt_lines = [
        "Below is a question along with the answer provided. Please evaluate the answer by highlighting its strengths,",
        "identifying any weaknesses, and suggesting improvements.",
        "Evaluation Criteria:",
        "- Clarity and Precision: Is the response clear, concise, and free of jargon?",
        "- Market and Business Insight: Does the answer demonstrate a solid understanding of the target market, customer needs, and competitive landscape?",
        "- Passion and Vision: Does it convey genuine commitment, a clear long-term vision, and enthusiasm?",
        "- Adaptability and Problem-Solving: Does it show responsiveness to feedback and a capability for overcoming challenges?",
        "",
        f"Question: {question}",
        f"Answer: {answer}",
        "",
        "Please provide your feedback as plain text, without markdown formatting, and ensure that your response is complete."
    ]
    prompt_text = "\n".join(prompt_lines)

    # Load environment variables from the root directory
    root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    dotenv_path = os.path.join(root_dir, ".env")
    load_dotenv(dotenv_path)

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in .env file.")
        sys.exit(1)

    client = OpenAI(api_key=openai_api_key)

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced evaluator who provides detailed, constructive feedback on answers to questions."
            },
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        max_tokens=250,
    )

    feedback = completion.choices[0].message.content.strip()
    return feedback

@answer_feedback.route("/judge-responses", methods=["POST"])
def judge_responses_route():
    data = request.get_json()
    if not data or "question" not in data or "answer" not in data:
        return jsonify({"error": "Missing required fields 'question' and 'answer'."}), 400
    
    question = data["question"]
    answer = data["answer"]
    feedback = judge_response(question, answer)
    
    return jsonify({"feedback": feedback}), 200
