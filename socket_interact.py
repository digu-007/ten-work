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
