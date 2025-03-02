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
        # r_msg = "GET /echo/banana HTTP/1.1\r\nHost: localhost:4221\r\n\r\n"
        parsed_msg = parse(r_msg)

        s_msg = create_msg(parsed_msg)

        deparsed_msg = deparse(s_msg)
        conn.send(deparsed_msg.encode())
        conn.close()

def deparse(msg):
    decoded = ""
    decoded += " ".join(msg["status_line"].values()) + "\r\n"
    if msg["headers"]:
        decoded += "\r\n".join(msg["headers"])
    decoded += "\r\n\r\n" 
    if msg["response_body"]:
        decoded += msg["response_body"]
    return decoded

def create_msg(msg):

    status_line = { 
        "http_version": msg["request_line"]["http_version"],     #First part of the status line is always the http version
        "return_code": None,                                     #3 digit return code
        "status": None                                           #Short status string
    }

    http_response = {
        "status_line": status_line,
        "headers": [],
        "response_body": "",
    }
    #split by / take first arg, the first arg is "" since it's /foo/bar = ["",foo,bar]
    #target = msg["request_line"]["request_target"].split("/")
    target = msg["request_line"]["request_target"]

    # host_args = msg["host"].split(":")
    # assert (host_args[0] == "Host")
    
    # target is right after GET 
    if target == "/":
        http_response["status_line"]["return_code"] = "200"
        http_response["status_line"]["status"] = "OK"


        return http_response
    elif target.startswith("/echo"):

        http_response["status_line"]["return_code"] = "200"
        http_response["status_line"]["status"] = "OK"
        
        # removing the /echo/
        content = target[6:]

        content_type = "Content-Type: text/plain"
        content_length = f"Content-Length: {len(content)}"

        http_response["headers"].append(content_type)
        http_response["headers"].append(content_length)

        http_response["response_body"] = content

        return http_response
    
    else:
        http_response["status_line"]["return_code"] = "404"
        http_response["status_line"]["status"] = "Not Found"

        return http_response

def parse(msg):
    args = msg.split("\r\n")
    args[0] = args[0].split(" ")


    # "\n\r".join(http_request)
    request_line = {
        "http_method": args[0][0],    # HTTP method
        "request_target": args[0][1], # Request target 
        "http_version": args[0][2],   # HTTP version
    }

    http_request = {
        "request_line": request_line,
        "headers":[],
    }

    for arg in args[1:]:
        http_request["headers"].append(arg)
    #print(http_request)
    return http_request


if __name__ == "__main__":
    main()
