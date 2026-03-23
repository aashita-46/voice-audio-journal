from audio_capture import record_audio, save_chunk
from transcriber import transcribe_audio
from summarizer import generate_summary
from history import save_session
from voice_auth import register_voice, verify_voice, PASSPHRASE

import os

TRANSCRIPT = ""

os.makedirs("chunks", exist_ok=True)

def run():
    global TRANSCRIPT

    print("🔐 Voice Authentication")
    print(f"👉 Please say: '{PASSPHRASE}'\n")

    choice = input("Type 'r' to register or 'l' to login: ").lower()

    # Record short voice sample
    print("🎤 Recording for authentication...")
    audio_data = next(record_audio())
    temp_file = "temp_voice.wav"
    save_chunk(audio_data, temp_file)

    # Transcribe what user said
    spoken_text = transcribe_audio(temp_file)
    print("📝 You said:", spoken_text)

    if choice == 'r':
        register_voice(temp_file)
        print("✅ Voice registered. Restart and login next time.")
        return

    elif choice == 'l':
        if not verify_voice(temp_file, spoken_text):
            print("❌ Access denied.")
            return
        else:
            print("✅ Voice + passphrase verified!\n")

    # ---------------- JOURNALING STARTS ---------------- #

    print("📓 Voice Journal Started...")
    print("🎤 Speak your thoughts. Press Ctrl+C to finish.\n")

    chunk_index = 0

    try:
        for audio_data in record_audio():
            filename = f"chunks/chunk_{chunk_index}.wav"
            save_chunk(audio_data, filename)

            print(f"\n🎧 Processing chunk {chunk_index}...")

            try:
                text = transcribe_audio(filename)
                print("📝 You said:", text)

                if text.strip():
                    TRANSCRIPT += " " + text

            except Exception as e:
                print("❌ Error:", e)

            chunk_index += 1

    except KeyboardInterrupt:
        print("\n🛑 Ending journal session...")

        if len(TRANSCRIPT.strip()) == 0:
            print("⚠️ No content recorded.")
            return

        print("\n🧠 Generating reflection summary...")
        summary = generate_summary(TRANSCRIPT)

        print("\n📄 Your Journal Entry:")
        print(TRANSCRIPT)

        print("\n✨ Reflection Summary:")
        print(summary)

        save_session(summary, TRANSCRIPT)
        print("\n💾 Journal saved!")


if __name__ == "__main__":
    run()