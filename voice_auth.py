from speechbrain.pretrained import SpeakerRecognition
import os

verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec"
)

REFERENCE_FILE = "voice_reference.wav"
PASSPHRASE = "my journal is private"


def register_voice(file_path):
    os.replace(file_path, REFERENCE_FILE)
    print("✅ Voice registered successfully!")


def verify_voice(file_path, transcribed_text):
    if not os.path.exists(REFERENCE_FILE):
        print("⚠️ No registered voice found.")
        return False

    # ✅ Step 1: Check passphrase
    if PASSPHRASE not in transcribed_text.lower():
        print("❌ Incorrect passphrase.")
        return False

    # ✅ Step 2: Check voice similarity
    score, _ = verification.verify_files(REFERENCE_FILE, file_path)
    print(f"🔍 Similarity score: {score}")

    return score > 0.75