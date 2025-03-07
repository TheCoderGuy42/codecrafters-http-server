import sys
import os
from io import StringIO
from app.requests.not_found import not_found
import codecs

def get_request(http_request, http_response):
      #split by / take first arg, the first arg is "" since it's /foo/bar = ["",foo,bar]
    #target = msg["request_line"]["request_target"].split("/")
    target = http_request["request_line"]["request_target"]

    # target is right after GET
    # if msg["request_line"]["http_method"] == "GET":
    #     http_response = get_request(http_response, target)

    http_response["status_line"]["return_code"] = "200"
    http_response["status_line"]["status"] = "OK"
    no_body = False

    if http_request["headers"].get("Accept-Encoding") != None:
        http_response["headers"]["Content-Type"] = "text/plain"
        compression_list = http_request["headers"]["Accept-Encoding"].split(",")
        for compression in compression_list:
            if compression.strip() == "gzip":
                http_response["headers"]["Content-Encoding"] = "gzip"
            else:
                no_body = True
        if no_body:
            return http_response

                


    if target == "/":
        pass


    elif target.startswith("/echo/"):
        
        # removing the /echo/
        content = target[6:]

        http_response["headers"]["Content-Type"] = "text/plain"
        http_response["headers"]["Content-Length"] = str(len(content))

        http_response["response_body"] = content

    
    elif target == "/user-agent":

        content = http_request["headers"]["User-Agent"]

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

            http_response["headers"]["Content-Type"] = "application/octet-stream"
            http_response["headers"]["Content-Length"] = os.path.getsize(target)

            http_response["response_body"] = content

            
        else:
            http_response = not_found(http_response)

    else:
        http_response = not_found(http_response)

    return http_response

