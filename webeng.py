import socket
import json
import struct
import pickle

# Physical Layer: Simulated using sockets and bit-level operations
class PhysicalLayer:
    def send(self, data, conn=None):
        binary_data = bin(int.from_bytes(data.encode(), 'big'))[2:]
        if conn:
            conn.sendall(binary_data.encode())  # Send over socket
        return binary_data
    
    def receive(self, conn):
        data = conn.recv(4096).decode()
        byte_length = (len(data) + 7) // 8  # Ensure correct byte size
        return int(data, 2).to_bytes(byte_length, 'big').decode()

# Data Link Layer: Implements MAC addressing and frame transmission
class DataLinkLayer:
    def send(self, data, mac_address="AA:BB:CC:DD:EE:FF"):
        frame = {"MAC": mac_address, "Payload": data}
        return json.dumps(frame)
    
    def receive(self, frame):
        frame = json.loads(frame)
        return frame["Payload"]

# Network Layer: Simulates IP addressing and packet routing
class NetworkLayer:
    def send(self, data, ip_address="192.168.1.1"):
        packet = {"IP": ip_address, "Payload": data}
        return json.dumps(packet)
    
    def receive(self, packet):
        packet = json.loads(packet)
        return packet["Payload"]

# Transport Layer: Implements TCP-like packet sequencing and error handling
class TransportLayer:
    def send(self, data, sequence=1):
        segment = {"Sequence": sequence, "Payload": data}
        return json.dumps(segment)
    
    def receive(self, segment):
        segment = json.loads(segment)
        return segment["Payload"]

# Session Layer: Manages connection states and synchronization
class SessionLayer:
    def send(self, data, session_id=1001):
        session_data = {"SessionID": session_id, "Payload": data}
        return json.dumps(session_data)
    
    def receive(self, session_data):
        session_data = json.loads(session_data)
        return session_data["Payload"]

# Presentation Layer: Handles encryption, compression, and encoding
class PresentationLayer:
    def send(self, data):
        encoded_data = pickle.dumps(data).hex()  # Convert to hex string
        return encoded_data
    
    def receive(self, encoded_data):
        return pickle.loads(bytes.fromhex(encoded_data))  # Convert back to original format

# Application Layer: Implements HTTP-like request-response communication
class ApplicationLayer:
    def send(self, data):
        request = {"HTTP": "GET", "Data": data}
        return json.dumps(request)
    
    def receive(self, request):
        request = json.loads(request)
        return request["Data"]

# OSI Model Simulation
class OSIModel:
    def __init__(self):
        self.physical = PhysicalLayer()
        self.data_link = DataLinkLayer()
        self.network = NetworkLayer()
        self.transport = TransportLayer()
        self.session = SessionLayer()
        self.presentation = PresentationLayer()
        self.application = ApplicationLayer()
    
    def transmit(self, data, conn):
        data = self.application.send(data)
        data = self.presentation.send(data)
        data = self.session.send(data)
        data = self.transport.send(data)
        data = self.network.send(data)
        data = self.data_link.send(data)
        data = self.physical.send(data, conn)
    
    def receive(self, conn):
        data = self.physical.receive(conn)
        data = self.data_link.receive(data)
        data = self.network.receive(data)
        data = self.transport.receive(data)
        data = self.session.receive(data)
        data = self.presentation.receive(data)
        data = self.application.receive(data)
        return data

# Server Code
def server():
    host = "127.0.0.1"
    port = 65432
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Server is listening on", host, port)
    
    conn, addr = server_socket.accept()
    print("Connected by", addr)
    osi = OSIModel()
    received_message = osi.receive(conn)
    print("Final Received Message:", received_message)
    conn.close()

# Client Code
def client():
    host = "127.0.0.1"
    port = 65432
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    osi = OSIModel()
    message = input("Enter message to send: ")  # User input for message
    print("Message Sent:", message)
    osi.transmit(message, client_socket)
    
    client_socket.close()

# Run either server() on one terminal or client() on another terminal