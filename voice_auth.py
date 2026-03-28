import os
import shutil
import numpy as np
import librosa
from scipy.spatial.distance import cosine

REFERENCE_FILE = "voice_reference.wav"
PASSPHRASE = "open"


def get_voice_embedding(file_path):
    """Extract MFCC features from audio file as a voice fingerprint."""
    y, sr = librosa.load(file_path, sr=16000, mono=True)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    return np.mean(mfcc, axis=1)  # Average across time = voice fingerprint


def register_voice(file_path):
    shutil.copy(file_path, REFERENCE_FILE)
    print("✅ Voice registered successfully!")


def verify_voice(file_path, transcribed_text):
    # Step 1: Check passphrase
    if PASSPHRASE not in transcribed_text.lower():
        print("❌ Incorrect passphrase. You said:", transcribed_text)
        print(f"👉 Please say: '{PASSPHRASE}'")
        return False

    # Step 2: Check if reference voice exists
    if not os.path.exists(REFERENCE_FILE):
        print("⚠️ No registered voice found. Please register first.")
        return False

    # Step 3: Compare voice fingerprints
    try:
        ref_embedding = get_voice_embedding(REFERENCE_FILE)
        cur_embedding = get_voice_embedding(file_path)

        similarity = 1 - cosine(ref_embedding, cur_embedding)
        print(f"🔍 Voice similarity score: {similarity:.4f}")

        if similarity > 0.80:
            print("✅ Voice recognized!")
            return True
        else:
            print(f"❌ Voice not recognized. Score: {similarity:.4f} (need > 0.80)")
            return False

    except Exception as e:
        print(f"⚠️ Voice check error: {e}")
        print("🔓 Falling back to passphrase-only auth.")
        return True