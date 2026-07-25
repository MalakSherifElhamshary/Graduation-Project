import os
import hashlib
import time
import json
import shutil
from datetime import datetime

# الأماكن اللي هنراقبها (زي الصورة)
WATCH_DIRS = ["./uploads", "./tools"]
LOG_FILE = "logs/fim_alerts.json"
BACKUP_DIR = "./backup_storage"

def get_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except:
        return None

def log_alert(event, file_path):
    alert = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": "FIM",
        "event": event,
        "file": file_path
    }
    if not os.path.exists('logs'): os.makedirs('logs')
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
    print(f"[!] ALERT: {event} in {file_path}")

def start_fim():
    print(f"[*] FIM Started. Monitoring: {WATCH_DIRS}")
    file_hashes = {}
    if not os.path.exists(BACKUP_DIR): os.makedirs(BACKUP_DIR)

    while True:
        for folder in WATCH_DIRS:
            if not os.path.exists(folder): os.makedirs(folder)
            for file in os.listdir(folder):
                path = os.path.join(folder, file)
                current_hash = get_hash(path)
                if current_hash is None: continue

                if path not in file_hashes:
                    log_alert("NEW_FILE", path)
                    shutil.copy(path, os.path.join(BACKUP_DIR, file))
                elif file_hashes[path] != current_hash:
                    log_alert("FILE_MODIFIED", path)
                
                file_hashes[path] = current_hash
        time.sleep(1)

if __name__ == "__main__":
    start_fim()
