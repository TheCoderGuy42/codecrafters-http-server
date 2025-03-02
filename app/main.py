import socket  # noqa: F401
import threading
import os
import sys

def handle_client(conn, addr):
    r_msg = conn.recv(1024).decode('utf-8')
    # r_msg = "GET /user-agent HTTP/1.1\r\nHost: localhost:4221\r\nUser-Agent: pineapple/raspberry\r\n\r\n"
    parsed_msg = parse(r_msg)

    s_msg = create_msg(parsed_msg)

    deparsed_msg = deparse(s_msg)
    conn.send(deparsed_msg.encode())
    conn.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()



def deparse(msg):
    decoded = ""
    decoded += " ".join(msg["status_line"].values()) + "\r\n"
    if msg["headers"]:
        decoded += "\r\n".join(f"{key}: {value}" for key,value in msg["headers"].items())
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
        "headers": {},
        "response_body": "",
    }

    # host_args = msg["host"].split(":")
    # assert (host_args[0] == "Host")
    


    #split by / take first arg, the first arg is "" since it's /foo/bar = ["",foo,bar]
    #target = msg["request_line"]["request_target"].split("/")
    target = msg["request_line"]["request_target"]

    # target is right after GET 
    if target == "/":
        http_response["status_line"]["return_code"] = "200"
        http_response["status_line"]["status"] = "OK"


    elif target.startswith("/echo/"):

        http_response["status_line"]["return_code"] = "200"
        http_response["status_line"]["status"] = "OK"
        
        # removing the /echo/
        content = target[6:]

        http_response["headers"]["Content-Type"] = "text/plain"
        http_response["headers"]["Content-Length"] = str(len(content))

        http_response["response_body"] = content

    
    elif target == "/user-agent":
        http_response["status_line"]["return_code"] = "200"
        http_response["status_line"]["status"] = "OK"

        content = msg["headers"]["User-Agent"]

        http_response["headers"]["Content-Type"] = "text/plain"
        http_response["headers"]["Content-Length"] = str(len(content))

        http_response["response_body"] = content

    elif target.startswith("/files/"):

        if "--directory" in sys.argv:
            index = sys.argv.index("--directory") + 1
            if index < len(sys.argv):
                directory = sys.argv[index]
                # ignoring /files/
                target = os.path.join(directory, target[7:])
        
        # if file exists, else read the file
        if os.path.isfile(target):
            with open(target, 'r') as file:
                content = file.read()

            http_response["status_line"]["return_code"] = "200"
            http_response["status_line"]["status"] = "OK"

            http_response["headers"]["Content-Type"] = "application/octet-stream"
            http_response["headers"]["Content-Length"] = os.path.getsize(target)

            http_response["response_body"] = content

        else:
            send404(http_response)

    else:
        http_response = send404(http_response)

    return http_response

def send404(msg):
    msg["status_line"]["return_code"] = "404"
    msg["status_line"]["status"] = "Not Found"
    return msg


def parse(msg):
    args = msg.split("\r\n")
    args[0] = args[0].split(" ")
    args = list(filter(None, args))


    # "\n\r".join(http_request)
    request_line = {
        "http_method": args[0][0],    # HTTP method
        "request_target": args[0][1], # Request target 
        "http_version": args[0][2],   # HTTP version
    }

    http_request = {
        "request_line": request_line,
        "headers":{},
    }

    for arg in args[1:]:
        # using a dictionary since it seems more resonable to
        pair = arg.split(":",1)
        http_request["headers"][pair[0]] = pair[1].strip()
    #print(http_request)
    return http_request


if __name__ == "__main__":
    main()
