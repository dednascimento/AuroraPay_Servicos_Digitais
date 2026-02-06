import os
from datetime import datetime

def log_debug(message: str):
    with open("debug.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"[{timestamp}] {message}\n")
