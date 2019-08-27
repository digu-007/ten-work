import socket
import threading
from queue import Queue

HOST = "0.0.0.0"
PORT = 8000
USERS = 10

print_lock = threading.Lock()

def get_server_socket():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen(USERS)
	return server


def handle_server_to_client_send(client_socket, client_address):
	with print_lock:
		source_file = input(f"Enter the file you want to send to {client_address}: ")
	chunk_size = 1024 * 1024 * 13 # 13 Mb
	file_data = open("server_test_data/" + source_file, "rb").read()
	sent = 0
	while sent < len(file_data):
		client_socket.send(file_data[sent : sent + chunk_size])
		sent += chunk_size
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
