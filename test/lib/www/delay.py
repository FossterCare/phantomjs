import io
from urllib import parse as urlparse
import time

def handle_request(req):
    url = urlparse.urlparse(req.path)
    delay = float(int(url.query))
    time.sleep(delay / 1000) # argument is in milliseconds

    body = "OK ({}ms delayed)\n".format(delay)
    req.send_response(200)
    req.send_header('Content-Type', 'text/plain')
    body_bytes = body.encode('utf-8')
    req.send_header('Content-Length', str(len(body_bytes)))
    req.end_headers()
    return io.BytesIO(body_bytes)
