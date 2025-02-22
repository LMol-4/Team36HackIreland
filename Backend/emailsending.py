import json
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(env_path)  
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Load the generated email JSON file
with open("generated_email.json", "r") as infile:
    email_data = json.load(infile)

# Create the email message
msg = EmailMessage()
msg["Subject"] = email_data["title"]
msg["From"] = sender_email
msg["To"] = email_data["email"]
msg.set_content(email_data["content"])

# Connect to Gmail's SMTP server and send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()               # Can be omitted; ensures connection is established
        smtp.starttls()           # Start TLS encryption
        smtp.ehlo()               # Re-identify as an encrypted connection
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)
    print("Email sent successfully!")
except Exception as e:
    print("An error occurred while sending the email:", e)
