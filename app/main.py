import socket  # noqa: F401
import threading
import os
import sys
from app.parsing import parse, deparse
from app.requests.get import get_request
from app.requests.post import post_request
from app.requests.not_found import not_found


def handle_client(conn, addr):
    r_msg = conn.recv(1024).decode('utf-8')
    # r_msg = "POST /files/orange_mango_pear_raspberry HTTP/1.1\r\nHost: localhost:4221\r\nContent-Length: 53\r\nContent-Type: application/octet-stream\r\n\r\nmango orange mango banana mango pineapple apple grape"
    parsed_msg = parse(r_msg)

    s_msg = create_msg(parsed_msg)

    deparsed_msg = deparse(s_msg)
    conn.send(deparsed_msg)
    conn.close()

def testing():
    r_msg = "POST /files/blueberry_blueberry_pineapple_pear HTTP/1.1\r\nHost: localhost:4221\r\nContent-Length: 75\r\nContent-Type: application/octet-stream\r\n\r\npineapple blueberry pineapple blueberry blueberry pear strawberry pineapple"
    parsed_msg = parse(r_msg)

    s_msg = create_msg(parsed_msg)

    deparsed_msg = deparse(s_msg)


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        conn, addr = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()



def create_msg(http_request):

    status_line = { 
        "http_version": http_request["request_line"]["http_version"],     #First part of the status line is always the http version
        "return_code": None,                                     #3 digit return code
        "status": None                                           #Short status string
    }

    http_response = {
        "status_line": status_line,
        "headers": {},
        "response_body": "",
    }

    # host_args = http_request["host"].split(":")
    # assert (host_args[0] == "Host")
    
    request_type = http_request["request_line"]["http_method"]
    if request_type == "GET":
        http_response = get_request(http_request, http_response)
    elif request_type == "POST":
        http_response == post_request(http_request, http_response)
    else:
        http_response = not_found(http_request, http_response)



    return http_response





if __name__ == "__main__":
    main()
