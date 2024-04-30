# Simple Python HTTP Server

In this challenge, you'll build a HTTP/1.1 server
that is capable of serving multiple clients.

Along the way you'll learn about TCP servers,
[HTTP request syntax](https://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html),
and more.


## Stages
- [X] Bind to a port
- [X] Respond with 200
- [X] Respond with 404
- [X] Respond with content
- [X] Parse headers
- [X] Concurrent connections
- [X] Get a file (read file content)
- [X] Post a file (write file content)


## Running locally
Python 3.11.9 with pipenv installed:

run ```./your_server.sh``` in one terminal session


## Tasks

Note: This section is for stage 1.

The entry point for your HTTP server implementation is in `app/main.py`. Study
and uncomment the relevant code, and push your changes to pass the first stage:

```sh
git add .
git commit -m "pass 1st stage" # any msg
git push origin master
```

Time to move on to the next stage!

Note: This section is for stages 2 and beyond.

1. Ensure you have `python (3.11)` installed locally
1. Run `./your_server.sh` to run your program, which is implemented in
   `app/main.py`.
1. Commit your changes and run `git push origin master` to submit your solution
   to CodeCrafters. Test output will be streamed to your terminal.
