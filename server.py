import socket
import threading
import socket_interact
from queue import Queue
from config import *

rooms_cnt = 0

active_users = set()
get_user_name = dict()
get_room_no = dict()
rooms = dict()

print_lock = threading.Lock()
active_users_lock = threading.Lock()
get_user_name_lock = threading.Lock()
get_room_no_lock = threading.Lock()
rooms_cnt_lock = threading.Lock()
rooms_lock = threading.Lock()


def register_client(client_socket, client_address, user_name):
	"""
	- Registers user_name with server
	- Maps: client_address -> user_name
	- Sends "BAD" to client if user_name already exists else room_no of the user
	"""
	global rooms_cnt
	with print_lock:
		print(f">>> {client_address} requested (user-name: {user_name}).")
	if user_name in active_users:
		with print_lock:
			print(f"(user-name: {user_name}) already exists.")
		socket_interact.send_message(client_socket, 1, "BAD")
	else:
		with active_users_lock:
			active_users.add(user_name)
		with get_user_name_lock:
			get_user_name[client_address] = user_name
		with rooms_cnt_lock:
			rooms_cnt += 1
		with rooms_lock:
			rooms[rooms_cnt] = [client_address]
		with get_room_no_lock:
			get_room_no[client_address] = rooms_cnt
		socket_interact.send_message(client_socket, 1, str(rooms_cnt))
		with print_lock:
			print(f"(user-name: {user_name}) registered.")
	with print_lock and active_users_lock:
		print(f"Active users: {active_users}")


def join_other_room(client_socket, client_address, desired_room):
	"""
	- Changes room of user to desired_room
	- Sends "BAD" to client if desired_room doesn't exist else "OK"
	"""
	with print_lock and get_user_name_lock and get_room_no_lock:
		print(f">>> (user: {get_user_name[client_address]}) requested room change from (room: {get_room_no[client_address]}) to (room: {desired_room}).")
	if desired_room not in rooms:
		with print_lock:
			print(f"(room: {desired_room}) doesn't exists.")
		socket_interact.send_message(client_socket, 2, "BAD")
	else:
		with get_room_no_lock:
			prv_room = get_room_no[client_address]
		with rooms_lock:
			rooms[prv_room].remove(client_address)
			if len(rooms[prv_room]) == 0:
				rooms.pop(prv_room)
			try:
				rooms[desired_room] += [client_address]
			except:
				rooms[desired_room] = [client_address] # Loopback (connect to current room)
		with get_room_no_lock:
			get_room_no[client_address] = desired_room
		socket_interact.send_message(client_socket, 2, "OK")
		with print_lock and get_user_name_lock:
			print(f"(user: {get_user_name[client_address]}) moved to (room: {desired_room}).")


def disconnect_room(client_socket, client_address):
	"""
	- Disconnects user from current room (with several users)
	- Moves him to new empty room
	"""
	global rooms_cnt
	with print_lock and get_user_name_lock and get_room_no_lock:
		print(f">>> (user: {get_user_name[client_address]}) requested to disconnect from (room: {get_room_no[client_address]}).")
	with get_room_no_lock:
		prv_room = get_room_no[client_address]
	with rooms_lock:
		if len(rooms[prv_room]) == 1:
			with print_lock:
				print(f"Single user in room. Failed disconnect request.")
			socket_interact.send_message(client_socket, 3, "BAD")
			return
		else:
			rooms[prv_room].remove(client_address)
	with rooms_cnt_lock:
		rooms_cnt += 1
		new_room = rooms_cnt
	with rooms_lock:
		rooms[new_room] = [client_address]
	with get_room_no_lock:
		get_room_no[client_address] = new_room
	socket_interact.send_message(client_socket, 3, str(prv_room) + " " + str(new_room))
	with print_lock and get_user_name_lock:
		print(f"(user: {get_user_name[client_address]}) disconnected from (room: {prv_room}) and moved to (room: {new_room}).")
	

def handle_client_receive(client_socket, client_address):
	"""
	- Handles requests from client
	"""
	while True:
		p_no, data_sz = socket_interact.receive_header(client_socket)
		if p_no == "001":
			user_name = socket_interact.receive_message(client_socket, data_sz)
			register_client(client_socket, client_address, user_name)
		elif p_no == "002":
			desired_room = int(socket_interact.receive_message(client_socket, data_sz))
			join_other_room(client_socket, client_address, desired_room)
		elif p_no == "003":
			disconnect_room(client_socket, client_address)
		else:
			continue


if __name__ == "__main__":
	server = socket_interact.get_server_socket()
	while True:
		(client_socket, client_address) = server.accept()
		with print_lock:
			print(f">>> Connection established at: {client_address}")
		th = threading.Thread(target = handle_client_receive, args = (client_socket, client_address), daemon = True)
		th.start()
