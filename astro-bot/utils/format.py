from datetime import datetime

def log_event(message, status="info"):
    emoji = {"info": "🛰️", "success": "✅", "error": "❌"}.get(status, "🔧")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {emoji} {message}")
