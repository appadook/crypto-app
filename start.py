# start.py
# This file is used to start the frontend and backend services.
# It is used to simplify the process of starting the services.
# It is also used to ensure that the services are started in the correct order.
# It is also used to ensure that the services are started in the correct terminal.
# It is also used to ensure that the services are started in the correct order.
# It is also used to ensure that the services are started in the correct terminal.


import subprocess
import time
import sys
import os
import platform

def start_frontend():
    system = platform.system()
    frontend_cmd = 'cd frontend && npx expo start --web'
    
    if system == 'Windows':
        # For Windows
        subprocess.Popen(['start', 'cmd', '/k', frontend_cmd], shell=True)
    elif system == 'Darwin':  # macOS
        # For macOS
        subprocess.Popen(['osascript', '-e', f'tell app "Terminal" to do script "{frontend_cmd}"'])
    elif system == 'Linux':
        # For Linux (this should work with most desktop environments)
        terminals = ['gnome-terminal', 'xterm', 'konsole']
        for terminal in terminals:
            try:
                subprocess.Popen([terminal, '--', 'bash', '-c', frontend_cmd])
                break
            except FileNotFoundError:
                continue

def run_services():
    try:
        # Start frontend in new terminal
        start_frontend()
        
        # Wait a few seconds to let frontend initialize
        print("Starting frontend in new terminal...")
        time.sleep(3)
        
        # Start backend in current terminal
        print("Starting backend in current terminal...")
        subprocess.run('python backend/run.py', shell=True)
        
    except KeyboardInterrupt:
        print("\nShutting down services...")
        sys.exit(0)

if __name__ == "__main__":
    run_services()