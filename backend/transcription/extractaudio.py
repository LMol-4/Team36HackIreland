#!/usr/bin/env python3
import sys
from moviepy import VideoFileClip


def extract_audio_from_file(video_file, output_audio):
    try:
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(output_audio)
        clip.close()
        print(f"Audio successfully extracted to {output_audio}")
    except Exception as e:
        print(f"Error extracting audio: {e}")


def extract_audio(video):
    try:
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(output_audio)
        clip.close()
        print(f"Audio successfully extracted to {output_audio}")
    except Exception as e:
        print(f"Error extracting audio: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extractaudio.py input_video.mp4 output_audio.mp3")
        sys.exit(1)
    video_file = sys.argv[1]
    output_audio = sys.argv[2]
    extract_audio_from_file(video_file, output_audio)
