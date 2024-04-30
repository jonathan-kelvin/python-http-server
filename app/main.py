import socket
import multiprocessing
import argparse
import os


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


def read_file_contents(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()  # Read the entire contents of the file
        return contents
    

def handle_connection(connection, client_address, i, directory):
    try:
        # Receive data from the client
        data = connection.recv(1024)
        print(f'Connection {i}: {client_address}')
        print('Received:', data.decode())

        # Process the received data
        decoded_data = data.decode()
        arr = decoded_data.split('\r\n')

        start_line = arr[0]
        method, path, version = start_line.split()
        headers = parse_headers(arr[1:])

        # Send a response back to the client
        response = "HTTP/1.1 404 NOT FOUND\r\nContent-Length: 0\r\n\r\n"

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

        elif path.startswith('/files/'):
            filename = path[7:]
            try:
                body = read_file_contents(os.path.join(directory, filename))
                status_line = "HTTP/1.1 200 OK\r\n"
                headers = f"Content-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\n"
                response = status_line + headers + body
            except FileNotFoundError:
                pass

        print(f"Response {i}: {response}")
        connection.sendall(response.encode())

    finally:
        # Clean up the connection
        connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=str, default=None)
    args = parser.parse_args()

    print('Directory:', args.directory)


    print('Starting server...')
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print('Server started')

    i = 0
    while True:
        connection, client_address = server_socket.accept() # wait for client
        i += 1
        process = multiprocessing.Process(target=handle_connection, args=(connection, client_address, i, args.directory))
        process.start()


if __name__ == "__main__":
    main()
