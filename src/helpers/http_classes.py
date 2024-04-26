from dataclasses import dataclass, field


@dataclass
class HttpRequest:
    method: str = None
    path: str = None
    version: str = None
    headers: dict[str, str] = field(default_factory=dict)
    body: str | bytes = ""


@dataclass
class HttpResponse:
    version: str = "HTTP/1.1"
    status_code: int = 200
    message: str = "OK"
    headers: dict[str, str] = field(default_factory=dict)
    body: str | bytes = None

    def set_header(self, key: str, value: str):
        self.headers[key] = value
        return self

    def encode(self) -> bytes:
        """Encodes the HttpResponse object into bytes suitable for sending over TCP.
        """
        response_line: str = f"{self.version} {self.status_code} {self.message}\r\n"
        if isinstance(self.body, bytes):
            bBody: bytes = self.body
        else:
            bBody: bytes = self.body.encode("utf-8") if self.body else b""

        if bBody and "Content-Length" not in self.headers:
            self.set_header("Content-Length", len(bBody))

        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        headers_end: str = "\r\n"

        response: bytes = (response_line + headers + headers_end).encode(
            "utf-8"
        ) + bBody

        return response