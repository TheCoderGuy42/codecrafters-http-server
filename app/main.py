import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr = server_socket.accept() # wait for client
        r_msg = conn.recv(1024).decode('utf-8')
        parsed_msg = parse(r_msg)

        s_msg = create_msg(parsed_msg)

        conn.send(s_msg.encode())
        conn.close()


def create_msg(msg):

    host_args = msg["host"].split(":")
    assert (host_args[0] == "Host")
    
    if msg["request_line"]["request_target"] == "/":
        return "HTTP/1.1 200 OK\r\n\r\n"
    else:
        return "HTTP/1.1 404 Not Found\r\n\r\n"

def parse(msg):
    args = msg.split("\r\n")
    args[0] = args[0].split(" ")


    # "\n\r".join(http_request)
    request_line = {
        "http_method": args[0][0],
        "request_target": args[0][1],
        "http_version": args[0][2]
    }

    http_request = {
        "request_line": request_line,
        "host": args[1],
        "user_agent": args[2],
        "accept": args[3]
    }
    #print(http_request)
    return http_request


if __name__ == "__main__":
    main()
