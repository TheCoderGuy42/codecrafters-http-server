import gzip

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
        "request_body":""
    }
    if request_line["http_method"] == "GET":
      for arg in args[1:]:
          # using a dictionary since it seems more resonable to
          pair = arg.split(":",1)
          http_request["headers"][pair[0]] = pair[1].strip()

    if request_line["http_method"] == "POST":
        for arg in args[1:-1]:
          # using a dictionary since it seems more resonable to
          pair = arg.split(":",1)
          http_request["headers"][pair[0]] = pair[1].strip()
        http_request["request_body"] = args[-1]

    return http_request

def deparse(msg):
    
    decoded = ""
    decoded += " ".join(msg["status_line"].values()) + "\r\n"

    if msg["response_body"] and msg["headers"].get("Content-Encoding") == "gzip":
        compressed_body = gzip_compression(msg["response_body"])
        msg["headers"]["Content-Length"] = str(len(compressed_body))


    if msg["headers"]:
        decoded += "\r\n".join(f"{key}: {value}" for key,value in msg["headers"].items())
        
    decoded += "\r\n\r\n" 
    decoded = decoded.encode()

    if msg["response_body"] and msg["headers"].get("Content-Encoding") == "gzip":
        decoded += compressed_body

    elif msg["response_body"]:
        decoded += msg["response_body"].encode() 

    return decoded

def gzip_compression(msg):

    compressed = gzip.compress(msg.encode('utf-8'))
    decompressed = gzip.decompress(compressed).decode()
    return compressed
