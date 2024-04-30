# Uncomment this to pass the first stage
import socket
import multiprocessing


def parse_headers(arr: list[str]) -> dict:
    headers_dict = {}
    for header in arr:
        if header == '':
            continue
        key, value = header.split(':', 1)
        key = key.strip()
        value = value.strip()
        headers_dict[key] = value
    return headers_dict


def handle_connection(connection, client_address):
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
        headers = parse_headers(arr[1:])


        print('Start line:', start_line)
        print('Path:', path)
        print('Headers:', headers)

        # Send a response back to the client
        response = "HTTP/1.1 404 NOT FOUND\r\n\r\n"

        if path == '/':
            response = "HTTP/1.1 200 OK\r\n\r\n"

        elif path.startswith('/echo/'):
            body = path[6:]
            status_line = "HTTP/1.1 200 OK\r\n"
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(body)}\r\n\n"
            response = status_line + headers + body

        elif path == '/user-agent' and 'User-Agent' in headers:
            body = headers['User-Agent']
            status_line = "HTTP/1.1 200 OK\r\n"
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(body)}\r\n\n"
            response = status_line + headers + body

        print('Response:', response)
        connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        connection, client_address = server_socket.accept() # wait for client
        process = multiprocessing.Process(target=handle_connection, args=(connection, client_address))
        process.start()


if __name__ == "__main__":
    main()
