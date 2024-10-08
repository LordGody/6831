import os
from socket import *
import sys

def webServer(port=13331):
    # Create the server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    try:
        # Bind the socket to the port and start listening for connections
        serverSocket.bind(("", port))
        serverSocket.listen(1)
        print(f"Server started on port {port}")

        while True:
            print("Waiting for connections...")
            try:
                # Accept incoming client connections
                connectionSocket, addr = serverSocket.accept()
                print(f"Connection established with {addr}")
            except timeout:
                print("Timeout occurred while waiting for a connection.")
                continue

            try:
                # Receive the client's request
                message = connectionSocket.recv(1024).decode()
                if not message:
                    connectionSocket.close()
                    continue

                # Parse the filename from the HTTP GET request
                filename = message.split()[1]

                # Check if the requested file exists, otherwise throw an error
                if not os.path.isfile(filename[1:]):
                    raise IOError

                # Read the requested file
                with open(filename[1:], "rb") as f:
                    content = f.read()

                # Prepare the HTTP response
                headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    "Server: SimplePythonServer\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                # Send the response (headers + content)
                connectionSocket.sendall(headers.encode() + content)

            except IOError:
                # Handle the case where the file is not found
                error_response = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=UTF-8\r\n"
                    "Server: SimplePythonServer\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                    "<html><body><h1>404 Not Found</h1></body></html>\r\n"
                )
                connectionSocket.sendall(error_response.encode())

            finally:
                # Close the connection
                connectionSocket.close()
                print(f"Connection with {addr} closed")

    except OSError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    webServer(13331)

