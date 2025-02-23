from openai import OpenAI
import os
from dotenv import load_dotenv
import sys

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

client = OpenAI(api_key=openai_api_key)

EVALUATION_INTRODUCTION = (
    "Below are several questions along with the answers provided. Please evaluate each answer, "
    "highlighting strengths, identifying weaknesses, and suggesting improvements.\n"
    "Evaluation Criteria if applicable:\n"
    "- Clarity and Precision: Is the response clear, jargon-free, and concise?\n"
    "- Market and Business Insight: Does it demonstrate a solid understanding of the target market, customer needs, and competitive landscape?\n"
    "- Passion and Vision: Does the answer convey genuine commitment, a clear long-term vision, and enthusiasm for the idea?\n"
    "- Adaptability and Problem-Solving: Does it show responsiveness to feedback and a strong capability for overcoming challenges?"
)

EVALUATOR_SYSTEM_MESSAGE = (
    "You are an experienced evaluator who provides detailed, constructive feedback on answers to questions."
)

def build_evaluation_prompt(questions, answers):
    if len(questions) != len(answers):
        raise ValueError("The number of questions and answers must be the same.")

    prompt_lines = [EVALUATION_INTRODUCTION, ""]
    for idx, (q, a) in enumerate(zip(questions, answers), start=1):
        prompt_lines.append(f"Question {idx}: {q}")
        prompt_lines.append(f"Answer {idx}: {a}")
        prompt_lines.append("")
    return "\n".join(prompt_lines)

def judge_responses(questions, answers):
    """
    Given a list of questions and a list of corresponding answers, this function constructs
    a prompt to have the OpenAI API evaluate the responses. It returns the evaluator's feedback.

    Args:
        questions (list of str): List of questions.
        answers (list of str): List of answers corresponding to each question.

    Returns:
        str: The feedback message generated by the OpenAI API.
    """
    prompt_text = build_evaluation_prompt(questions, answers)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": EVALUATOR_SYSTEM_MESSAGE},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=2000,
    )

    return completion.choices[0].message