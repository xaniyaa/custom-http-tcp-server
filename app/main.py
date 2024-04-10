import socket
from dataclasses import field, dataclass
import threading


CRLF = "\r\n"

@dataclass
class HttpRequest:
    method: str = None
    path: str = None
    version: str = None
    headers: dict[str, str] = field(default_factory=dict)
    body: str = None

@dataclass
class HttpResponse:
    version: str = "HTTP/1.1"
    status_code: int = 200
    message: str = "OK"
    headers: dict[str, str] = field(default_factory=dict)
    body: str = ""

    def set_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def encode(self) -> bytes:
        """
        Encodes the HttpResponse object into bytes suitable for sending over TCP.
        """
        response_line: str = (
            f"{self.version} {self.status_code} {self.message}\r\n"
        )

        bBody = self.body.encode("utf-8") if self.body else b""

        if bBody and "Content-Length" not in self.headers:
            self.set_header("Content-Length", len(bBody))
        
        headers = "".join(
            f"{key}: {value}\r\n" for key, value in self.headers.items()
        )
        
        headers_end: str = "\r\n"

        response: bytes = (response_line + headers + headers_end).encode(
            "utf-8"
        ) + bBody

        return response


def handle_client(client_socket: socket.socket, client_address: str, buffer_size: int = 128) -> None:
    
    print(f"Client connected on {client_address} ...")
    buffer: str = ""
    headers_end: bool = False
    content_length: int = None
    request = HttpRequest()
    while True:
        try:
            request_bytes = client_socket.recv(buffer_size)
            if not request_bytes:
                print(f"Connection closed by client: {client_address}")
                break
            data: str = request_bytes.decode()
            buffer += data
            log_str: str = buffer.replace("\\r\\n", "\\\\r\\\\n")
            print(f"Buffer right now: {log_str}")
            if (not headers_end and "\r\n\r\n" in buffer):  # end of headers is a an empty line
              
                # fmt: off
                headers_part, buffer = buffer.split("\r\n\r\n", 1)
                # fmt: on
                headers_lines = headers_part.split("\r\n")
                request.method, request.path, request.version = headers_lines[0].split()
                headers_end = True
                for line in headers_lines[1:]:  # skip the start line
                    key, value = line.split(":", 1)
                    request.headers[key.strip()] = value.strip()
                    if key.lower() == "content-length":
                        content_length = int(value.strip())
                print("Finished parsing all request headers ...")
            if not headers_end:
                continue
            if content_length is None:
                break
            if len(buffer) >= content_length:
                request.body = buffer[:content_length]
                break
        except Exception as e:
            print(f"Error with {client_address}: {e}")
            break
    print(f"Received request: {request} ...")
    if "/" == request.path:
        response = HttpResponse(status_code=200, message="OK")
    elif request.path.startswith("/echo"):
        text: str = request.path.split("/", 2)[-1]
        response = HttpResponse(
            status_code=200,
            message="OK",
            body=text,
        ).set_header("Content-Type", "text/plain")
    else:
        response = HttpResponse(status_code=404, message="Not found")

    print(f"Will response with {response}")
    client_socket.send(response.encode())
    client_socket.close()


def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen()
    threads = []
    print(f"[+] Server started with port {4221}...")
    try:
        while True:
            client_socket, client_address = server_socket.accept()  # wait for client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, 1024),
            )
            client_thread.daemon = True
            client_thread.start()
            threads.append(client_thread)
    finally:
        server_socket.close()
        for thread in threads:
            thread.join()  # Wait for all client threads to finish
        print("Server has been gracefully shutdown.")

if __name__ == "__main__":
    main()
            
