import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

client = OpenAI(api_key=openai_api_key)

HACKATHON_CRITERIA = (
    "Evaluate the pitch based on the following hackathon criteria:\n"
    "- Problem Definition & Relevance: How clearly is the problem defined and its relevance to the track explained?\n"
    "- Innovation & Creativity: Assess the uniqueness and creativity of the idea.\n"
    "- Technical Feasibility & Execution: Evaluate the quality, practicality, and execution of the prototype or demo.\n"
    "- Impact & Scalability: Determine the potential impact and scalability of the solution.\n"
)

PITCHDECK_CRITERIA = (
    "As an experienced venture capitalist, evaluate the following business pitch based on these criteria if relevant:\n\n"
    "1. Problem & Solution Clarity:\n"
    "   - How clearly is the market problem defined?\n"
    "   - Is the proposed solution innovative, scalable, and compelling?\n\n"
    "2. Market Opportunity & Business Model:\n"
    "   - Assess the size, growth potential, and segmentation of the target market.\n"
    "3. Traction & Financial Performance:\n"
    "   - Review key performance indicators, early customer adoption, and revenue trends.\n"
    "4. Competitive Advantage & Risks:\n"
    "   - Determine the startup’s unique value proposition and defensibility (competitive moat).\n"
    "   - Identify potential risks and the team’s strategies for risk mitigation.\n\n"
    "Please provide a thorough, data-driven analysis with clear justification for each criterion used."
)

EVALUATION_PROMPT_TEMPLATE = (
    "Evaluate the following pitch text as a {pitch_type} pitch.\n\n"
    "{criteria_text}\n"
    "Please provide a detailed evaluation that includes:\n"
    "- Strengths of the pitch.\n"
    "- Areas for improvement.\n"
    "- Specific suggestions on how to enhance each aspect of the pitch.\n"
    "- Reference specific lines from the pitch where improvements can be made.\n"
    "- Assign a score out of 100 based on the overall quality of the pitch.\n\n"
    "Return your response in a structured JSON format with the following keys:\n"
    "score, strengths, areas_for_improvement, suggestions, line_references, summary.\n\n"
    "Pitch Text:\n"
    "{pitch_text}\n"
)

def load_pitch_text(args):
    """
    Load the pitch text either directly from command-line input or from a file.
    """
    if args.input_text:
        return args.input_text
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        print("No pitch text provided.")
        sys.exit(1)

def create_prompt(pitch_text, pitch_type):
    """
    Create a prompt for the OpenAI model that instructs it to evaluate the pitch
    based on predefined criteria for the specified pitch type.
    """
    # Choose criteria text based on the pitch type
    if pitch_type.lower() == "hackathon":
        criteria_text = HACKATHON_CRITERIA
    elif pitch_type.lower() in ["pitchdeck", "pitch deck"]:
        criteria_text = PITCHDECK_CRITERIA
    else:
        criteria_text = "Unknown pitch type. Please choose either 'hackathon' or 'pitch deck'."

    prompt = EVALUATION_PROMPT_TEMPLATE.format(
        pitch_type=pitch_type,
        criteria_text=criteria_text,
        pitch_text=pitch_text
    )
    return prompt

def evaluate_pitch(pitch_text, pitch_type):
    """
    Call the OpenAI API to evaluate the pitch and return a JSON object containing the evaluation.
    """
    prompt = create_prompt(pitch_text, pitch_type)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that evaluates pitch quality."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        result_text = completion.choices[0].message.content.strip()
        try:
            result_json = json.loads(result_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON. Raw response:")
            print(result_text)
            sys.exit(1)
        return result_json
    except Exception as e:
        print(f"Error evaluating pitch: {e}")
        sys.exit(1)

def get_feedback(transcription: str, pitch_type: str):
    return evaluate_pitch(transcription, pitch_type)
