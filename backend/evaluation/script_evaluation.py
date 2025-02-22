#!/usr/bin/env python3
import os
import sys
import json
import argparse
from dotenv import load_dotenv
from openai import OpenAI

# Load the API key from the .env file in the root directory.
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

# Instantiate the client using the new API syntax.
client = OpenAI(api_key=openai_api_key)

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
        print("No pitch text provided. Use --input_text or --file.")
        sys.exit(1)

def create_prompt(pitch_text, pitch_type):
    """
    Create a prompt for the OpenAI model that instructs it to evaluate the pitch
    based on predefined criteria for the specified pitch type.
    """
    if pitch_type.lower() == "hackathon":
        criteria_text = (
            "Evaluate the pitch based on the following hackathon criteria:\n"
            "- Problem Definition & Relevance: How clearly is the problem defined and its relevance explained?\n"
            "- Innovation & Creativity: Assess the uniqueness and creativity of the idea.\n"
            "- Technical Feasibility & Execution: Evaluate the quality, practicality, and execution of the prototype or demo.\n"
            "- Impact & Scalability: Determine the potential impact and scalability of the solution.\n"
        )
    elif pitch_type.lower() in ["pitchdeck", "pitch deck"]:
        criteria_text = (
            "As an experienced venture capitalist, evaluate the following business pitch based on these criteria:\n"
            "- Problem & Solution Clarity: Assess how clearly the market problem is defined and how compelling the proposed solution is.\n"
            "- Market Opportunity & Business Model: Evaluate the market size, target audience, revenue streams, and competitive landscape.\n"
            "- Team & Execution Capability: Consider the experience and execution ability of the founding team.\n"
        )
    else:
        criteria_text = "Unknown pitch type. Please choose either 'hackathon' or 'pitch deck'."

    prompt = (
        f"Evaluate the following pitch text as a {pitch_type} pitch.\n\n"
        f"{criteria_text}\n"
        "Please provide a detailed evaluation that includes:\n"
        "- Strengths of the pitch.\n"
        "- Areas for improvement.\n"
        "- Specific suggestions on how to enhance each aspect of the pitch.\n"
        "- Reference specific lines from the pitch where improvements can be made.\n"
        "- Assign a score out of 100 based on the overall quality of the pitch.\n\n"
        "Return your response in a structured JSON format with the following keys:\n"
        "score, strengths, areas_for_improvement, suggestions, line_references, summary.\n\n"
        "Pitch Text:\n"
        f"{pitch_text}\n"
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
        # Access the message content from the new API response format.
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


def get_feedback(transcripton: str, pitch_type: str):
    return evaluate_pitch(transcripton, pitch_type)

def main():
    parser = argparse.ArgumentParser(description="Evaluate a pitch using OpenAI API.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input_text", type=str, help="Pitch text input directly.")
    group.add_argument("--file", type=str, help="Path to a file containing the pitch text.")
    parser.add_argument("--type", type=str, required=True, choices=["hackathon", "pitchdeck", "pitch deck"],
                        help="Type of pitch: 'hackathon' or 'pitch deck'.")
    parser.add_argument("--json_output", action="store_true", help="Output JSON evaluation to a file.")
    parser.add_argument("--output_file", type=str, help="File path to write the JSON output to.")
    parser.add_argument("--summary_output", action="store_true", help="Print a formatted summary output for human readability.")
    args = parser.parse_args()

    pitch_text = load_pitch_text(args)
    evaluation = evaluate_pitch(pitch_text, args.type)

    # If json_output flag is set, write the evaluation JSON to a file if an output file path is provided.
    if args.json_output:
        json_str = json.dumps(evaluation, indent=4)
        if args.output_file:
            try:
                with open(args.output_file, "w", encoding="utf-8") as f:
                    f.write(json_str)
                print(f"JSON output written to {args.output_file}")
            except Exception as e:
                print(f"Error writing JSON to file: {e}")
                sys.exit(1)
        else:
            # If no output file is specified, print the JSON to the terminal.
            print(json_str)

    if args.summary_output:
        print("\nFormatted Summary:")
        print("Score: ", evaluation.get("score"))
        print("\nStrengths:")
        for s in evaluation.get("strengths", []):
            print("-", s)
        print("\nAreas for Improvement:")
        for a in evaluation.get("areas_for_improvement", []):
            print("-", a)
        print("\nSuggestions:")
        for s in evaluation.get("suggestions", []):
            print("-", s)
        print("\nLine References:")
        for ref in evaluation.get("line_references", []):
            print("-", ref)
        print("\nSummary:")
        print(evaluation.get("summary"))

    # If neither json_output nor summary_output is set, print a basic summary.
    if not args.json_output and not args.summary_output:
        print("Score: ", evaluation.get("score"))
        print("Summary: ", evaluation.get("summary"))

if __name__ == "__main__":
    main()
