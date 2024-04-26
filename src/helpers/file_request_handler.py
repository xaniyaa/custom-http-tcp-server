import os
from src.helpers.http_classes import HttpRequest, HttpResponse


def handle_get_file_request(request: HttpRequest, dir: str) -> HttpResponse:
    filename: str = request.path.split("/")[-1]
    file_path: str = os.path.join(dir, filename)

    if not os.path.exists(file_path):
        return HttpResponse(status_code=404, message="Not found")

    with open(file_path, "rb") as file:
        data: bytes = file.read()

    return HttpResponse(status_code=200, message="OK", body=data).set_header(
        "Content-Type", "application/octet-stream"
    )

def handle_post_file_request(request: HttpRequest, dir: str) -> HttpResponse:
    filename: str = request.path.split("/", 2)[-1]
    file_path: str = os.path.join(dir, filename)

    with open(file_path, "wb") as file:
        file.write(request.body.encode())

    return HttpResponse(status_code=201,message="Created",)