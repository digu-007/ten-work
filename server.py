import socket
import threading
from queue import Queue
from socket_interact import get_server_socket
from config import *

print_lock = threading.Lock()


def handle_server_to_client_send(client_socket, client_address):
	with print_lock:
		source_file = input(f"Enter the file you want to send to {client_address}: ")
	file_data = open("tests/server_test_data/" + source_file, "rb").read()
	sent = 0
	while sent < len(file_data):
		client_socket.send(file_data[sent : sent + CHUNK_SIZE])
		sent += CHUNK_SIZE
	with print_lock:
		print(f"Sent file {source_file} to {client_address}")
	client_socket.close()


if __name__ == "__main__":
	server = get_server_socket()
	while True:
		(client_socket, client_address) = server.accept()
		with print_lock:
			print(f"Connection established at: {client_address}")
		th = threading.Thread(target = handle_server_to_client_send, args = (client_socket, client_address), daemon = True)
		th.start()
