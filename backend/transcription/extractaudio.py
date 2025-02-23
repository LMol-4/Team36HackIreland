import moviepy.video.VideoClip as VideoFileClip
def extract_audio_from_file(video_file, output_audio):
    try:
        clip = VideoFileClip(video_file)
        clip.audio.write_audiofile(output_audio)
        clip.close()
        print(f"Audio successfully extracted to {output_audio}")
    except Exception as e:
        print(f"Error extracting audio: {e}")