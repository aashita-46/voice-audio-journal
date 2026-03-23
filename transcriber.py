import whisper
import os

os.environ["PATH"] += os.pathsep + r"C:\Users\Ninad Naik\OneDrive\Pictures\ffmpeg\bin"

print("Loading Whisper model...")
model = whisper.load_model("base")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]