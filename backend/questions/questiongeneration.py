import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

def generate_questions(transcript):
    """
    Given a pitch transcript, this function uses the GPT-4o-mini model to generate a list of 10 potential questions 
    that might be asked of the pitcher.
    """
    # Compute the path to the root directory (one level up) to load the .env file
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
        "that experienced investors or a panel of judges might ask the presenter. The questions should critically assess key aspects of the business, focusing on the following dimensions:\n\n"
        "1. Business Model: Revenue streams, cost structure, and value proposition.\n"
        "2. Scalability: Growth potential, operational constraints, and market demand.\n"
        "3. Market Validation: Customer adoption, traction, and product-market fit.\n"
        "4. Competitive Landscape: Differentiation, barriers to entry, and threats from incumbents.\n"
        "5. Financial Projections: Revenue forecasts, cost assumptions, and funding needs.\n"
        "6. Risk Management: Identifiable risks, contingency plans, and regulatory considerations.\n"
        "7. Execution Strategy: Team expertise, go-to-market strategy, and operational efficiency.\n\n"
        f"{transcript}\n\n"
        "Each question should demonstrate a deep understanding of the pitch, critically examine both strengths and potential weaknesses, "
        "and challenge the presenter to substantiate their claims with data, market insights, or strategic foresight."
        "Format it question nicely in a json object."
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an experienced venture capitalist, who is skilled at analyzing pitches"},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <transcript_file>")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    
    with open(transcript_file, 'r') as file:
        transcript = file.read()
    
    questions = generate_questions(transcript)
    print(questions)