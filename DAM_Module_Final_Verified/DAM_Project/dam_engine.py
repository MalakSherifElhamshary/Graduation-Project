import json
import time
import os
from datetime import datetime

# المسارات الأساسية للربط مع الويبسايت
LOG_FILE = "logs/dam_alerts.json"

def log_alert(user, query, severity):
    alert = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": "DAM",
        "event": "Database Query Detected",
        "user": user,
        "query": query,
        "severity": severity
    }
    # إنشاء فولدر اللوجات لو مش موجود
    if not os.path.exists('logs'): os.makedirs('logs')
    
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(alert) + "\n")
    print(f"[!!!] DAM ALERT: {user} executed {query} ({severity})")

def start_monitoring():
    print("[*] Database Activity Monitoring (DAM) is Live...")
    # محاكاة لعمليات بتحصل فعلياً
    mock_queries = [
        ("admin", "SELECT * FROM payroll", "Low"),
        ("hacker_node", "DROP TABLE users", "Critical"),
        ("dev_user", "DELETE FROM logs", "High")
    ]
    
    for user, query, sev in mock_queries:
        log_alert(user, query, sev)
        time.sleep(3) # عشان تشوفي التنبيهات وهي بتظهر واحدة واحدة

if __name__ == "__main__":
    start_monitoring()
