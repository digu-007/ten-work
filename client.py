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
	if message == "BAD":
		return True
	else:
		print(f"Joined (room: {message}).")
		return False


def register_client(conn):
	"""
	- Registers a client with a unique user-name
	- Returns a unique user-name
	"""
	user_name = input(">>> Enter a user-name: ")
	while user_name_taken(conn, user_name):
		user_name = input(f">>> (user-name: {user_name}) is already taken. Enter a different user-name: ")
	return user_name
	

def join_other_room(conn, room_no):
	"""
	- Takes user to some other room (Lobby where his friends maybe present :P)
	"""
	socket_interact.send_message(conn, 2, str(room_no))
	p_no, data_sz = socket_interact.receive_header(conn)
	message = socket_interact.receive_message(conn, data_sz)
	if message == "OK":
		print(f"Joined (room: {room_no}).")
	else:
		print(f"(room: {room_no}) doesn't exist.")


def disconnect_room(conn):
	"""
	- Disconnects user from current room (with several users)
	- Moves him to new empty room
	"""
	socket_interact.send_message(conn, 3, "")
	p_no, data_sz = socket_interact.receive_header(conn)
	message = socket_interact.receive_message(conn, data_sz)
	if message == "BAD":
		print(f"You can't disconnect from a room with single user.")
	else:
		prv_room, new_room = map(int, message.split())
		print(f"Disconnected from (room: {prv_room}).")
		print(f"Joined (room: {new_room}).")


if __name__ == "__main__":
	conn = socket_interact.get_client_socket()
	user_name = register_client(conn)
	print(">>> ", end = "")
	while True:
		cmd = input().split()
		try:
			typ = cmd[0]
			if typ == "connect" and len(cmd) == 2:
				join_other_room(conn, int(cmd[1]))
			elif typ == "disconnect" and len(cmd) == 1:
				disconnect_room(conn)
			elif typ == "quit":
				break
			else:
				print("Unknown command entered.")
		except:
			print("Exception: Unknown command entered.")
		print(">>> ", end = "")
	conn.close()
