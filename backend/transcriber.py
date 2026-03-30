import whisper

model = whisper.load_model("tiny")

def transcribe_audio(path):
    result = model.transcribe(path)
    return result["text"]