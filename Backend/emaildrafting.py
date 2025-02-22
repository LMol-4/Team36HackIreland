import json
import re
from openai import OpenAI
from dotenv import load_dotenv
import os

# Construct the path to the 'apikeys.env' file which is located in the main directory
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'apikeys.env')
load_dotenv(env_path)  
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client (pass in your API key if needed)
client = OpenAI(api_key=api_key)

# Example JSON for the recipient
recipient_json = '''
{
  "person": {
    "name": "Jane Doe",
    "bio": "Jane Doe is a software engineer with a passion for building scalable web applications. She has over 10 years of experience in the industry and is proficient in various programming languages and technologies.",
    "contact": {
      "email": "jane.doe@example.com",
      "phone": "+15551234567"
    }
  }
}
'''

# Example JSON for the sender
sender_json = '''
{
  "person": {
    "name": "John Smith",
    "bio": "John Smith is an entrepreneur with a strong background in tech startups. He has built and sold multiple companies and is looking to invest in innovative projects.",
    "looking_for": "John is looking for a talented software engineer to join his team and co-found his next startup.",
    "contact": {
      "email": "john.smith@example.com",
      "linkedin": "https://www.linkedin.com/in/johnsmith",
      "twitter": "@johnsmith",
      "github": "https://github.com/johnsmith",
      "website": "https://www.johnsmith.com",
      "phone": "+15559876543"
    }
  }
}
'''

# Convert JSON strings to Python dictionaries
recipient_data = json.loads(recipient_json)
sender_data = json.loads(sender_json)

# Define the email type as a variable (this can be changed as required)
email_type = "organizes a coffe meet up"

# Construct the prompt for the chat API using the provided JSON details and email type
prompt = f"""
Draft an email that {email_type}.

Recipient Details:
- Name: {recipient_data['person']['name']}
- Bio: {recipient_data['person']['bio']}
- Email: {recipient_data['person']['contact']['email']}
- Phone: {recipient_data['person']['contact']['phone']}

You are:
- Name: {sender_data['person']['name']}
- Bio: {sender_data['person']['bio']}
- Looking for: {sender_data['person']['looking_for']}
- Email: {sender_data['person']['contact']['email']}
- LinkedIn: {sender_data['person']['contact']['linkedin']}
- Twitter: {sender_data['person']['contact']['twitter']}
- GitHub: {sender_data['person']['contact']['github']}
- Website: {sender_data['person']['contact']['website']}
- Phone: {sender_data['person']['contact']['phone']}

Please draft a concise, friendly email that meets the requirments of the email type.
Return your response strictly in JSON format with the following keys:
- "email": the recipient's email address.
- "title": the subject line of the email.
- "content": the body of the email.
"""

# Create the chat completion using the OpenAI client
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that drafts emails to help organise meetups between people. Please return your response in a valid JSON format as requested."},
        {"role": "user", "content": prompt}
    ]
)

# Retrieve the generated response
response_text = completion.choices[0].message.content

# Remove Markdown code fences if present
if response_text.startswith("```"):
    response_text = re.sub(r"^```(?:json)?\n", "", response_text)
    response_text = re.sub(r"\n```$", "", response_text)

# Attempt to parse the response as JSON
try:
    generated_email = json.loads(response_text)
except json.JSONDecodeError as e:
    print("Failed to parse JSON from the response:", e)
    generated_email = {"error": "Invalid JSON output", "raw_output": response_text}

# Print the generated email JSON
print(json.dumps(generated_email, indent=2))

# Optionally, write the JSON output to a file
with open("generated_email.json", "w") as outfile:
    json.dump(generated_email, outfile, indent=2)