# Remote Computer Control

A Python-based GUI application for remotely controlling a computer using a client-server architecture.

## Features
- List and manage processes/applications
- Capture and save screenshots
- Start/stop keylogger
- Shutdown/restart system
- Monitor system resources
- Transfer files

## Requirements
- Python 3.x
- Install dependencies:
  ```bash
  pip install psutil pyautogui pynput pillow PyQt5
  ```

## Installation
1. Clone the repository or download the source code.
2. Install required packages using the command above.
3. Ensure the server (`server.py`) is running on the target machine.

## Usage
1. Run the server on the target machine:
   ```bash
   python server.py
   ```
2. Run the client GUI on your machine:
   ```bash
   python client.py
   ```
3. Use the tabbed interface to control the remote system.

## Configuration
- Update `HOST` and `PORT` in `client.py` to match the server address (default: `127.0.0.1:5000`).

## Notes
- Requires network connectivity between client and server.
- No authentication or encryption is implemented (use in a secure environment).

## Contributors
- [Vinh Trung THIEU](https://github.com/tvtrungg)
- [Huynh Man NGUYEN](https://github.com/nhman2002) 