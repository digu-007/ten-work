import socket
from socket_interact import get_client_socket
from config import *


def receive_file(conn, tar_file):
    get = b""
    while True:
        rec_data = conn.recv(CHUNK_SIZE)
        if len(rec_data) == 0:
            break
        else:
            get = get + rec_data
    open("tests/client_test_data/" + tar_file, "wb").write(get)


if __name__ == "__main__":
    conn = get_client_socket()
    tar_file = input("Enter the name of target file: ")
    print(f"Target: {tar_file}")
    receive_file(conn, tar_file)
    print("File received :)")
    conn.close()
