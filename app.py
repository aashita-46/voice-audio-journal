from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
import os
import tempfile
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "sunset_journal_secret"
CORS(app)

from transcriber import transcribe_audio
from summarizer import generate_summary
from voice_auth import register_voice, verify_voice, PASSPHRASE
from history import save_session, get_all_sessions, init_db
from audio_capture import save_chunk
import numpy as np

init_db()
os.makedirs("chunks", exist_ok=True)
os.makedirs("recordings", exist_ok=True)

TRANSCRIPT = ""
chunk_index = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/register", methods=["POST"])
def register():
    if "audio" not in request.files:
        return jsonify({"success": False, "message": "No audio file"}), 400

    audio_file = request.files["audio"]
    temp_path = "temp_register.wav"
    audio_file.save(temp_path)

    try:
        spoken_text = transcribe_audio(temp_path)
        register_voice(temp_path)
        return jsonify({
            "success": True,
            "message": "Voice registered successfully!",
            "heard": spoken_text
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/login", methods=["POST"])
def login():
    if "audio" not in request.files:
        return jsonify({"success": False, "message": "No audio file"}), 400

    audio_file = request.files["audio"]
    temp_path = "temp_login.wav"
    audio_file.save(temp_path)

    try:
        spoken_text = transcribe_audio(temp_path)
        verified = verify_voice(temp_path, spoken_text)

        if verified:
            session["authenticated"] = True
            return jsonify({
                "success": True,
                "message": "Access granted!",
                "heard": spoken_text
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Passphrase not recognized. You said: {spoken_text}",
                "heard": spoken_text
            })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/record_chunk", methods=["POST"])
def record_chunk():
    global TRANSCRIPT, chunk_index

    if "audio" not in request.files:
        return jsonify({"success": False, "message": "No audio"}), 400

    audio_file = request.files["audio"]
    filename = f"chunks/chunk_{chunk_index}.wav"
    audio_file.save(filename)

    try:
        text = transcribe_audio(filename)
        if text.strip():
            TRANSCRIPT += " " + text
        chunk_index += 1
        return jsonify({
            "success": True,
            "text": text.strip(),
            "full_transcript": TRANSCRIPT.strip()
        })
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/finish", methods=["POST"])
def finish():
    global TRANSCRIPT, chunk_index

    if not TRANSCRIPT.strip():
        return jsonify({"success": False, "message": "No content recorded"}), 400

    try:
        summary = generate_summary(TRANSCRIPT)
        save_session(summary, TRANSCRIPT)

        result = {
            "success": True,
            "transcript": TRANSCRIPT.strip(),
            "summary": summary
        }

        TRANSCRIPT = ""
        chunk_index = 0

        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/api/discard", methods=["POST"])
def discard():
    global TRANSCRIPT, chunk_index
    TRANSCRIPT = ""
    chunk_index = 0
    return jsonify({"success": True, "message": "Session discarded"})


@app.route("/api/history", methods=["GET"])
def history():
    try:
        sessions = get_all_sessions()
        entries = []
        for row in sessions:
            entries.append({
                "timestamp": row[0],
                "transcript": row[1],
                "summary": row[2]
            })
        return jsonify({"success": True, "entries": entries})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)