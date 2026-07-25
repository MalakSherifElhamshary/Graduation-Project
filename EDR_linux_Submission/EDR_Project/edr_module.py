import os
import time
import json
from datetime import datetime

# 1. تحميل القواعد من الملف
try:
    with open('edr_rules.json', 'r') as f:
        config = json.load(f)
except:
    config = {"suspicious_commands": ["nmap", "nc", "whoami", "sudo", "chmod"], "log_output": "logs/edr_alerts.json"}

SUSPICIOUS_CMDS = config['suspicious_commands']
LOG_FILE = config['log_output']
# مسار ملف الهيستوري في كالي
HIST_FILE = os.path.expanduser("~/.zsh_history")

def log_event(command):
    alert = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": "EDR",
        "event": "Suspicious Command Detected",
        "command": command,
        "severity": "High"
    }
    # إنشاء مجلد اللوجات لو مش موجود
    if not os.path.exists('logs'): os.makedirs('logs')
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
    print(f"\a[!!!] EDR ALERT: {command}") # الـ \a بتعمل صوت تنبيه بسيط

def start_monitoring():
    print("[*] EDR Engine Started... Monitoring Terminal Behavior (Real-time)")
    
    # تحديد نقطة البداية (نهاية الملف الحالية)
    last_size = os.path.getsize(HIST_FILE) if os.path.exists(HIST_FILE) else 0

    while True:
        time.sleep(0.1) # فحص فائق السرعة (10 مرات في الثانية)
        if os.path.exists(HIST_FILE):
            current_size = os.path.getsize(HIST_FILE)
            if current_size > last_size:
                with open(HIST_FILE, "r", errors="ignore") as f:
                    f.seek(last_size)
                    new_lines = f.readlines()
                    for line in new_lines:
                        # تنظيف السطر من إضافات zsh اللعينة
                        clean_cmd = line.split(';')[-1].strip() if ';' in line else line.strip()
                        if any(trigger in clean_cmd for trigger in SUSPICIOUS_CMDS):
                            log_event(clean_cmd)
                last_size = current_size

if __name__ == "__main__":
    start_monitoring()
