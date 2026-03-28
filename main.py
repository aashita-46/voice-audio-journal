from audio_capture import record_audio, save_chunk
from transcriber import transcribe_audio
from summarizer import generate_summary
from history import save_session, print_history
from voice_auth import register_voice, verify_voice, PASSPHRASE

import os

os.makedirs("chunks", exist_ok=True)

TRANSCRIPT = ""


def authenticate():
    """Handle voice registration or login. Returns True if authenticated."""
    print("\n🔐 Voice Authentication")
    print(f"👉 Please say the passphrase: '{PASSPHRASE}'\n")

    choice = input("Type 'r' to register your voice, 'l' to login: ").strip().lower()
    if choice not in ('r', 'l'):
        print("❌ Invalid choice.")
        return False

    print("🎤 Recording voice sample...")
    audio_data = next(record_audio())
    temp_file = "temp_voice.wav"
    save_chunk(audio_data, temp_file)

    spoken_text = transcribe_audio(temp_file)
    print(f"📝 You said: {spoken_text}")

    if choice == 'r':
        register_voice(temp_file)
        print("✅ Voice registered! Restart the app and login.")
        return False  # Force restart after registration

    elif choice == 'l':
        if verify_voice(temp_file, spoken_text):
            print("✅ Voice + passphrase verified!\n")
            return True
        else:
            print("❌ Access denied. Try again.")
            return False


def record_journal():
    """Record journal audio in chunks, transcribe each, return full transcript."""
    global TRANSCRIPT
    TRANSCRIPT = ""

    print("📓 Voice Journal Started!")
    print("🎤 Speak your thoughts. Press Ctrl+C when you're done.\n")

    chunk_index = 0

    try:
        for audio_data in record_audio():
            filename = f"chunks/chunk_{chunk_index}.wav"
            save_chunk(audio_data, filename)
            print(f"\n🎧 Processing chunk {chunk_index}...")

            try:
                text = transcribe_audio(filename)
                if text.strip():
                    print(f"📝 You said: {text}")
                    TRANSCRIPT += " " + text
            except Exception as e:
                print(f"❌ Transcription error: {e}")

            chunk_index += 1

    except KeyboardInterrupt:
        print("\n🛑 Recording stopped.")

    return TRANSCRIPT.strip()


def run():
    print("=" * 50)
    print("        🎙️  Voice Journal System")
    print("=" * 50)

    # Optional: view history before starting
    view_history = input("\nWould you like to view past entries first? (y/n): ").strip().lower()
    if view_history == 'y':
        print_history()

    # Step 1: Authenticate
    if not authenticate():
        return

    # Step 2: Record & Transcribe
    transcript = record_journal()

    if not transcript:
        print("⚠️ No content recorded. Session not saved.")
        return

    # Step 3: Summarize
    print("\n🧠 Generating reflection summary...")
    summary = generate_summary(transcript)

    # Step 4: Display results
    print("\n" + "=" * 50)
    print("📄 Your Journal Entry:")
    print(transcript)
    print("\n✨ Reflection Summary:")
    print(summary)
    print("=" * 50)

    # Step 5: Save to SQLite
    save_session(summary, transcript)
    print("\n✅ Journal session complete!")


if __name__ == "__main__":
    run()