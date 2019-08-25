import socket

HOST = "172.16.22.45"
PORT = 8000

def get_connection():
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))
    return conn


def receive_file(conn, tar_file):
    chunk_size = 1024 * 1024 * 1024
    get = b""
    while True:
        rec_data = conn.recv(chunk_size)
        if len(rec_data) == 0:
            break
        else:
            get = get + rec_data
    open(tar_file, "wb").write(get)


if __name__ == "__main__":
    conn = get_connection()
    # print(conn)
    tar_file = input("Enter the name of target file: ")
    print("Target: {}".format(tar_file))
    receive_file(conn, tar_file)
    print("File received :)")
    conn.close()