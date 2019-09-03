import socket
from config import *


def get_server_socket():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(("0.0.0.0", PORT))
	server.listen(USERS)
	return server
	
	
def get_client_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    return client
    

def get_header(p_no, data_sz):
	p_no = str(p_no)
	p_no = (3 - len(p_no)) * "0" + p_no
	data_sz = str(data_sz)
	data_sz = (3 - len(data_sz)) * "0" + data_sz
	header = p_no + "," + data_sz
	return header
	

def send_message(conn, p_no, data):
	header = get_header(p_no, len(data))
	message = header + data
	# ~ print(f"Header: {header}    |    Data: {data}")
	message = message.encode()
	# ~ print(f"Message: {message}")
	conn.sendall(message)
	

def receive_header(conn):
	header = receive_message(conn, HEADER_SIZE)
	p_no, data_sz = header.split(",")
	return p_no, int(data_sz)


def receive_message(conn, rem):
	data = bytes()
	while rem > 0:
		buff = conn.recv(min(CHUNK_SIZE, rem))
		data += buff
		rem -= len(buff)
	data = data.decode()
	return data
