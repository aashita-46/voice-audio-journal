import os
import shutil

REFERENCE_FILE = "voice_reference.wav"
PASSPHRASE = "my journal is private"


def register_voice(file_path):
    shutil.copy(file_path, REFERENCE_FILE)
    print("✅ Voice registered successfully!")


def verify_voice(file_path, transcribed_text):
    if PASSPHRASE in transcribed_text.lower():
        print("✅ Passphrase matched!")
        return True
    else:
        print("❌ Incorrect passphrase. You said:", transcribed_text)
        print(f"👉 Please say: '{PASSPHRASE}'")
        return False