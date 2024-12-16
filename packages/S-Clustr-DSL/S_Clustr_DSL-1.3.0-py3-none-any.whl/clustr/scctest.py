import sys
import socket
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton,
    QWidget, QGridLayout, QVBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QTimer

class TcpClientThread(QThread):
    message_received = pyqtSignal(int, str)
    connection_status = pyqtSignal(int, str)
    connection_successful = pyqtSignal()

    def __init__(self, server_ip, server_port, client_id):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.running = True
        self.client_id = client_id

    def run(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.server_ip, self.server_port))
            self.connection_status.emit(self.client_id, 'connected')
            self.send_message('{"TYPE": "Arduino"}\r\n')
            self.connection_successful.emit()
            while self.running:
                try:
                    data = self.socket.recv(1024).decode('utf-8').strip()
                    if data:
                        self.handle_message(data)
                except socket.timeout:
                    pass
        except socket.error as e:
            self.connection_status.emit(self.client_id, f'Error: {str(e)}')
        finally:
            if self.socket:
                self.socket.close()
                if self.running:
                    self.message_received.emit(self.client_id, "black")

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode('utf-8'))
        except socket.error as e:
            self.connection_status.emit(self.client_id, f'Error: {str(e)}')

    def handle_message(self, message):
        try:
            block_id, action = map(int, message.split(':'))
            if block_id >= 1 and block_id <= 5:
                color = "green" if action == 1 else "red" if action == 2 else "black"
                self.message_received.emit(block_id - 1 + (self.client_id * 5), color)
        except ValueError:
            print(f"Invalid message format: {message}")

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()

class TcpClientBlock(QWidget):
    def __init__(self, block_id):
        super().__init__()
        self.block_id = block_id
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: red;")
        self.layout = QVBoxLayout()
        self.status_label = QLabel(f"Block {self.block_id + 1}", self)
        self.layout.addWidget(self.status_label)
        self.setLayout(self.layout)
    
    @pyqtSlot(int, str)
    def set_color(self, block_id, color):
        if block_id != self.block_id:
            return
        print(f"Setting color for block {self.block_id + 1} to {color}")
        self.setStyleSheet(f"background-color: {color};")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TCP Client Blocks")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.ip_port_input = QLineEdit(self)
        self.ip_port_input.setPlaceholderText("Enter TCP server IP:Port")
        self.layout.addWidget(self.ip_port_input, 0, 0, 1, 2)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_clients)
        self.layout.addWidget(self.start_button, 0, 2)

        self.disconnect_button = QPushButton("Disconnect", self)
        self.disconnect_button.clicked.connect(self.disconnect_clients)
        self.layout.addWidget(self.disconnect_button, 0, 3)

        self.blocks = []
        self.client_threads = []
        self.current_client = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.start_next_client)

        for i in range(6):
            client_blocks = [TcpClientBlock(j) for j in range(5)]
            self.blocks.append(client_blocks)
            for j, block in enumerate(client_blocks):
                self.layout.addWidget(block, i + 1, j)

    def start_clients(self):
        server_ip, server_port = self.get_server_info()
        self.client_threads = []
        self.current_client = 0
        self.start_next_client()

    def start_next_client(self):
        if self.current_client < 6:
            server_ip, server_port = self.get_server_info()
            client_thread = TcpClientThread(server_ip, server_port, self.current_client)
            client_thread.message_received.connect(self.set_block_color)
            client_thread.connection_status.connect(self.handle_status)
            client_thread.connection_successful.connect(self.on_client_connected)
            self.client_threads.append(client_thread)
            client_thread.start()
        else:
            print("All clients started.")
            self.timer.stop()

    def on_client_connected(self):
        self.current_client += 1
        self.timer.start(1000)

    @pyqtSlot(int, str)
    def set_block_color(self, block_id, color):
        client_index = block_id // 5
        block_index = block_id % 5
    
        if client_index < len(self.blocks) and block_index < len(self.blocks[client_index]):
            self.blocks[client_index][block_index].set_color(block_index, color)
        else:
            print(f"Index out of range: client_index={client_index}, block_index={block_index}")

    def handle_status(self, client_id, status):
        print(f"Connection status for client {client_id}: {status}")

    def disconnect_clients(self):
        for client_thread in self.client_threads:
            client_thread.stop()
            client_thread.wait()

        self.client_threads = []

    def get_server_info(self):  
        ip_port = self.ip_port_input.text().split(':')
        return ip_port[0], int(ip_port[1])

    def closeEvent(self, event):
        self.disconnect_clients()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
