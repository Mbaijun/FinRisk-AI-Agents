import sys
import subprocess
import threading
import time

def print_banner():
print("=" * 50)
print("FinRisk-AI-Agents Launcher")
print("=" * 50)

def install_deps():
print("Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def start_api():
print("Starting API: http://localhost:8000")
subprocess.run([sys.executable, "-m", "api.fastapi_app"])

def start_ui():
print("Starting UI: http://localhost:8501")
subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/dashboard.py", "--server.port", "8501"])

def main():
print_banner()
print("1. Install dependencies")
print("2. Start API")
print("3. Start UI")
print("4. Start all services")
print("0. Exit")

text

澶嶅埗

涓嬭浇
choice = input("Choice: ").strip()

if choice == "1":
    install_deps()
elif choice == "2":
    start_api()
elif choice == "3":
    start_ui()
elif choice == "4":
    install_deps()
    print("Starting all services...")
    api_thread = threading.Thread(target=start_api, daemon=True)
    ui_thread = threading.Thread(target=start_ui, daemon=True)
    api_thread.start()
    ui_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping services...")
elif choice == "0":
    print("Goodbye!")
    sys.exit(0)
if name == "main":
main()
