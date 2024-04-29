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

        # Process the received data (optional)

        # Send a response back to the client
        response = "HTTP/1.1 200 OK\r\n\r\n"
        connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()


if __name__ == "__main__":
    main()