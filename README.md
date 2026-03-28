# 🎙️ Voice Audio Journal

A **Flask-based AI-powered voice journaling app** that allows users to record audio, transcribe it, and generate summaries — all in one place.

---

## 🚀 Features

* 🎤 Record voice entries
* 📝 Convert speech to text (Speech Recognition)
* 🧠 AI-powered summarization
* 🔐 Voice authentication (optional)
* 📂 Store and manage journal history

---

## 🛠️ Tech Stack

* **Backend:** Flask (Python)
* **Frontend:** HTML, CSS, JavaScript
* **AI/ML:** Transformers, SpeechRecognition
* **Deployment:** Render (backend), Vercel (frontend)

---

## 📁 Project Structure

```
voice-audio-journal/
│
├── frontend/              # Frontend UI
│
├── backend/               # Flask backend
│   ├── app.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── voice_auth.py
│   ├── requirements.txt
│   ├── Procfile
│   └── templates/
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/voice-audio-journal.git
cd voice-audio-journal/backend
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Run the app

```bash
python app.py
```

---

## 🌐 Deployment

### Backend (Render)

* Root Directory: `backend`
* Build Command:

```bash
pip install -r requirements.txt
```

* Start Command:

```bash
gunicorn app:app
```

---

### Frontend (Vercel)

* Root Directory: `frontend`

---

## ⚠️ Notes

* Audio files and database (`.wav`, `.db`) are ignored using `.gitignore`
* For production, consider using:

  * Cloud storage (for audio)
  * PostgreSQL instead of SQLite

---

## 📌 Future Improvements

* 📱 Mobile-friendly UI
* ☁️ Cloud storage integration
* ⚡ Background processing (Celery)
* 🔒 Enhanced authentication

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

This project is open-source and available under the MIT License.

---

👩‍💻 Author

**Aashita Jolly**


✨ If you like this project, consider giving it a star!
