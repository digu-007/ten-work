import socket

HOST = "127.0.0.1"
PORT = 8000

def get_listening_socket():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    return conn


def receive_file(conn, tar_file):
    chunk_size = 1024 * 1024 * 13
    get = b""
    while True:
        rec_data = conn.recv(chunk_size)
        if len(rec_data) == 0:
            break
        else:
            get = get + rec_data
    open("client_test_data/" + tar_file, "wb").write(get)


if __name__ == "__main__":
    conn = get_listening_socket()
    tar_file = input("Enter the name of target file: ")
    print(f"Target: {tar_file}")
    receive_file(conn, tar_file)
    print("File received :)")
    conn.close()
