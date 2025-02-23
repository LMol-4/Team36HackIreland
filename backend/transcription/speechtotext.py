import os
import sys
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

def transcribe_audio(audio_file):
    try:
        with open(audio_file, "rb") as audio:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )
        return transcription
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        sys.exit(1)