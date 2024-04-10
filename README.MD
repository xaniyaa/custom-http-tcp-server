# Simple custom HTTP TCP server from scratch

It can handle following commands

| Route | Response | Response code | Body |
| ----- | ------ | ------ | ------ | 
| GET  / | HTTP response  | 200 | - |
| GET  /echo | HTTP response | 200 | Request Body |
| GET  /user-agent | HTTP response | 200 | User Agent Header e.g "curl/7.64.1" |
| GET  /files/<filename> | HTTP response | 200 | File's contents |
| POST  /files/<filename> | HTTP response |201 | None |


# Quick run for UNIX-like OS
-  Install python
-  Clone repository
-  ```bash server.sh --directory <directory>```. Directory flag is your absolute path to application.

Credits to codecrafters team and their users.