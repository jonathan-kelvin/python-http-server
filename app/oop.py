import argparse
import asyncio
import enum
import os

BODY_SEPARATOR = b"\r\n\r\n"


class StatusCode(enum.Enum):
    OK = 200, "OK"
    CREATED = 201, "Created"
    NOT_FOUND = 404, "Not Found"


class Headers(dict):
    def __str__(self) -> str:
        return "\n".join(f"{k}: {v}" for k, v in self.items())
    

class Request:
    def __init__(self, content: bytes) -> None:
        if BODY_SEPARATOR in content:
            headers_bytes, self.body = content.split(BODY_SEPARATOR)
        else:
            headers_bytes, self.body = content, b""
        headers = headers_bytes.decode("utf-8")
        headers_lines = headers.strip().split("\n")
        self.method, self.path, self.http_version = headers_lines[0].strip().split(" ")
        self.headers = Headers(
            {
                k: v
                for k, v in (line.strip().split(": ") for line in headers_lines[1:])
                if k
            }
        )


class Response:
    def __init__(
        self,
        request: Request,
        status_code: StatusCode,
        headers: dict | None = None,
        content: str | bytes = "",
    ) -> None:
        self.request = request
        self.status_code = status_code
        self.content = content
        self.headers = Headers(headers or {})


    def to_bytes(self) -> bytes:
        print(
            f"{self.request.http_version} {self.status_code.value[0]} {self.status_code.value[1]}\r\n\r\n{self.content}"
        )
        if isinstance(self.content, str):
            self.headers["Content-Length"] = str(len(self.content))
            self.headers["Content-Type"] = "text/plain"
            content = self.content.encode("utf-8")
        elif isinstance(self.content, bytes):
            self.headers["Content-Length"] = str(len(self.content))
            self.headers["Content-Type"] = "application/octet-stream"
            content = self.content
        else:
            raise TypeError(f"Unknown content type: {type(self.content)}")
        response = (
            f"{self.request.http_version} {self.status_code.value[0]} {self.status_code.value[1]}\r\n{self.headers}\r\n\r\n"
        ).encode("utf-8")
        response += content
        return response
    

class Server:
    def __init__(self, directory: str | None = None) -> None:
        self.directory = directory


    async def serve_forever(self, host: str, port: int):
        server = await asyncio.start_server(self._handle_client, host, port)
        async with server:
            await server.serve_forever()


    def _handle(self, request_content: bytes) -> Response:
        r = Request(request_content)
        if r.path == "/":
            return Response(r, StatusCode.OK)
        elif r.path.startswith("/echo"):
            return Response(r, StatusCode.OK, content=r.path.removeprefix("/echo/"))
        elif r.path == "/user-agent":
            return Response(r, StatusCode.OK, content=r.headers["User-Agent"])
        elif r.method == "GET" and r.path.startswith("/files"):
            assert self.directory is not None
            file_path = self.directory + r.path.removeprefix("/files/")
            if not os.path.isfile(file_path):
                return Response(r, StatusCode.NOT_FOUND)
            return Response(
                r,
                StatusCode.OK,
                content=open(
                    self.directory + r.path.removeprefix("/files/"), "rb"
                ).read(),
            )
        elif r.method == "POST" and r.path.startswith("/files"):
            assert self.directory is not None
            file_path = self.directory + r.path.removeprefix("/files/")
            with open(file_path, "wb") as f:
                f.write(r.body)
            return Response(r, StatusCode.CREATED)
        else:
            return Response(r, StatusCode.NOT_FOUND)
        

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        print("Got connection from", writer.get_extra_info("peername"))
        while True:
            data = await reader.read(1024)
            if not data:
                break
            
            writer.write(self._handle(data).to_bytes())
            await writer.drain()

        writer.close()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=str, default=None)
    args = parser.parse_args()

    await Server(args.directory).serve_forever("localhost", 4221)


if __name__ == "__main__":
    asyncio.run(main())
    