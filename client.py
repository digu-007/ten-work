import socket
import socket_interact
from config import *


def user_name_taken(conn, user_name):
	"""
	- Return True if user_name is already registered with server else False
	"""
	socket_interact.send_message(conn, 1, user_name)
	p_no, data_sz = socket_interact.receive_header(conn)
	message = socket_interact.receive_message(conn, data_sz)
	return message == "BAD"


def register_client(conn):
	"""
	- Registers a client with a unique user-name
	- Returns a unique user-name
	"""
	user_name = input("Enter a user-name: ")
	while user_name_taken(conn, user_name):
		user_name = input(f"User-name {user_name} is already taken. Enter a different user-name: ")
	return user_name
	

if __name__ == "__main__":
    conn = socket_interact.get_client_socket()
    user_name = register_client(conn)
    # ~ while True:
		
    conn.close()
