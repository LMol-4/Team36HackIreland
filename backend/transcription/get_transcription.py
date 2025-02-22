import os
import tempfile
from .extractaudio import extract_audio_from_file
from .speechtotext import transcribe_audio

def get_transcription(video_path: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
         audio_path = temp_audio.name
    try:
         extract_audio_from_file(video_path, audio_path)
         result = transcribe_audio(audio_path)
         transcript_text = getattr(result, "text", None) or result.get("text", "")
         return transcript_text
    finally:
         if os.path.exists(audio_path):
              os.remove(audio_path)
