import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"
def save_session(summary, transcript):
    data = []

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "journal_entry": transcript.strip(),
        "reflection": summary
    }

    data.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)