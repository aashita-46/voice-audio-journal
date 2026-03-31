import whisper
import os

os.environ["PATH"] += os.pathsep + r"C:\Users\HP\Downloads\ffmpeg\bin"

model = whisper.load_model("tiny")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]