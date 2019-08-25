import socket

HOST = "0.0.0.0"
PORT = 8000
USERS = 1

def get_connection():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen(USERS)
	return server


def send_file(client_socket, source_file):
	chunk_size = 1024 * 1024 * 1024
	file_data = open(source_file, "rb").read()
	sent = 0
	while sent < len(file_data):
		client_socket.send(file_data[sent : sent + chunk_size])
		sent += chunk_size
	print("Sent file: {}".format(source_file))
  

if __name__ == "__main__":
	server = get_connection()
	(client_socket, client_address) = server.accept()
	print("Connection established")
	source_file = input("Enter the file you want to send: ")
	send_file(client_socket, source_file)
	server.close()
