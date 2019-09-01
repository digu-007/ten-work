import socket
import threading
import socket_interact
from queue import Queue
from config import *

active_users = set()
get_user_name = dict()

print_lock = threading.Lock()
active_users_lock = threading.Lock()
get_user_name_lock = threading.Lock()


def register_client(client_socket, client_address, user_name):
	"""
	- Registers user_name with server
	- Maps: client_address -> user_name
	- Sends "OK" to client if registry complete else "BAD"
	"""
	print(f"Active users: {active_users}")
	print(f"Current request user: {user_name}")
	if user_name in active_users:
		with print_lock:
			print(f"User-name {user_name} already exists.")
		socket_interact.send_message(client_socket, 1, "BAD")
	else:
		with active_users_lock:
			active_users.add(user_name)
		with get_user_name_lock:
			get_user_name[client_address] = user_name
		socket_interact.send_message(client_socket, 1, "OK")
		with print_lock:
			print(f"User-name {user_name} registered.")


def handle_client_receive(client_socket, client_address):
	"""
	- Handles requests from client
	"""
	while True:
		p_no, data_sz = socket_interact.receive_header(client_socket)
		if p_no == "001":
			user_name = socket_interact.receive_message(client_socket, data_sz)
			register_client(client_socket, client_address, user_name)
		else:
			continue


if __name__ == "__main__":
	server = socket_interact.get_server_socket()
	while True:
		(client_socket, client_address) = server.accept()
		with print_lock:
			print(f"Connection established at: {client_address}")
		th = threading.Thread(target = handle_client_receive, args = (client_socket, client_address), daemon = True)
		th.start()
