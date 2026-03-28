import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import queue

SAMPLE_RATE = 16000
CHUNK_DURATION = 10
SILENCE_THRESHOLD = 0.0001  # adjust if needed

audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def is_silent(audio):
    return np.abs(audio).mean() < SILENCE_THRESHOLD

def normalize_audio(audio):
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val
    return audio

def record_audio():
    print("Recording started. Speak clearly...")

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
        while True:
            frames = []

            for _ in range(int(SAMPLE_RATE / 1024 * CHUNK_DURATION)):
                frames.append(audio_queue.get())

            audio_data = np.concatenate(frames, axis=0)

            # Skip silent chunks
            if is_silent(audio_data):
                continue

            # Normalize for better Whisper input
            audio_data = normalize_audio(audio_data)

            yield audio_data

def save_chunk(audio_data, filename):
    write(filename, SAMPLE_RATE, audio_data)