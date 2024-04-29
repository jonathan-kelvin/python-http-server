# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    connection, client_address = server_socket.accept() # wait for client

    try:
        print('Connection from', client_address)

        # Receive data from the client
        data = connection.recv(1024)
        print('Received:', data.decode())

        # Process the received data
        decoded_data = data.decode()
        arr = decoded_data.split('\r\n')
        print('Arr:', arr)
        start_line = arr[0]
        method, path, version = start_line.split()
        print('Path:', path)

        # Send a response back to the client
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"

        if path == '/':
            response = "HTTP/1.1 200 OK\r\n\r\n"

        elif path.startswith('/echo/'):
            text = path[6:]
            status_line = "HTTP/1.1 200 OK\r\n"
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(text)}\r\n\n"
            body = text + '\r\n\r\n'
            response = status_line + headers + body

        connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()


if __name__ == "__main__":
    main()
