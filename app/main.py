import socket


def main():
    print("[+] App started!")
    
    while True:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        client_socket, _ = server_socket.accept()
        
        with client_socket as sock:
            data, _, _, _ = sock.recvmsg(1024)
            print(f"[DEBUG] data before decode: {data}")
            data = data.decode()
            print(f"[DEBUG] data after decode: {data}")
            request_path = extract_headers(data)
            if request_path == "/":
                sock.sendmsg([("HTTP/1.1 200 OK\r\n\r\n").encode()])
            else:
                sock.sendmsg([("HTTP/1.1 404 Not found\r\n\r\n").encode()])
            


def extract_headers(header_string: str) -> str:
    header_lines = header_string.split("\r\n")
    start_line = header_lines[0].split(" ")
    method, path, version = start_line
    return path


if __name__ == "__main__":
    main()
