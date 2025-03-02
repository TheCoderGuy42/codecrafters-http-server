import sys
import os
from app.requests.not_found import not_found


def post_request(http_request, http_response):

  target = http_request["request_line"]["request_target"]

  if target.startswith("/files/"):
      if "--directory" in sys.argv:
          index = sys.argv.index("--directory") + 1
          if index < len(sys.argv):
              directory = sys.argv[index]
              # ignoring /files/
              target = os.path.join(directory, target[7:])
      # if file exists, else read the file
      content = http_request["request_body"]

      try:
        with open(target, 'w') as file:
            file.write(content)
      except:
        http_response = not_found(http_response)

      http_response["status_line"]["return_code"] = "201"
      http_response["status_line"]["status"] = "Created"

      http_response["headers"]["Content-Type"] = "application/octet-stream"
      http_response["headers"]["Content-Length"] = str(len(content))

      http_response["response_body"] = content




  else:
      http_response = not_found(http_response)

  return http_response