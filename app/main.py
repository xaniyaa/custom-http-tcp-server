import socket


def main():
    print("[+] App started!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, _ = server_socket.accept()
    bytes = "HTTP/1.1 200 OK\r\n\r\n".encode("utf-8")
    client_socket.send(bytes)

if __name__ == "__main__":
    main()
