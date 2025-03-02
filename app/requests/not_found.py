def not_found(msg):
    msg["status_line"]["return_code"] = "404"
    msg["status_line"]["status"] = "Not Found"

    msg["headers"] = {}
    msg["response_body"] = ""

    return msg