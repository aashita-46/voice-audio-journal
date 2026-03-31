import os
import sys
sys.path.insert(0, "/opt/render/project/src")

import openai_whisper as whisper

model = whisper.load_model("tiny")

def transcribe_audio(file_path):
    result = model.transcribe(file_path)
    return result["text"]