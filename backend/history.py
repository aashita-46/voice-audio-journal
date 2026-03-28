import sqlite3
from datetime import datetime

DB_FILE = "journal.db"


def init_db():
    """Create the journal table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            journal_entry TEXT NOT NULL,
            reflection TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_session(summary, transcript):
    """Save a journal session to the SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO journal (timestamp, journal_entry, reflection)
        VALUES (?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        transcript.strip(),
        summary
    ))
    conn.commit()
    conn.close()
    print(f"💾 Entry saved to {DB_FILE}")


def get_all_sessions():
    """Retrieve all journal sessions from the database."""
    init_db()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, journal_entry, reflection FROM journal ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows


def print_history():
    """Pretty-print all past journal entries."""
    sessions = get_all_sessions()
    if not sessions:
        print("📭 No journal entries found.")
        return
    for i, (ts, entry, reflection) in enumerate(sessions, 1):
        print(f"\n{'='*50}")
        print(f"📅 Entry #{i} — {ts}")
        print(f"📝 Journal:\n{entry}")
        print(f"✨ Reflection:\n{reflection}")
    print(f"\n{'='*50}")