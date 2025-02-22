#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

# Compute the path to the root directory (one level up) to load the .env file
root_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

# Retrieve the OpenAI API key from the .env file.
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    print("Error: OPENAI_API_KEY not found in .env file.")
    sys.exit(1)

# Initialize the OpenAI client with the API key using the new format.
client = OpenAI(api_key=openai_api_key)

def transcribe_audio(audio_file):
    try:
        with open(audio_file, "rb") as audio:
            # Call the audio transcription endpoint with the new client syntax.
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )
        return transcription
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python speechtotext.py input_audio_file [output_text_file]")
        sys.exit(1)
    audio_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "transcription.txt"

    result = transcribe_audio(audio_file)
    transcript_text = getattr(result, "text", None) or result.get("text", "")

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        print(f"Transcript successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing transcript to file: {e}")
        sys.exit(1)
