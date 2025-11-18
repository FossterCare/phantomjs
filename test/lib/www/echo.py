import io
import json
from urllib import parse as urlparse

def handle_request(req):
    url = urlparse.urlparse(req.path)
    headers = {}
    for name, value in req.headers.items():
        headers[name] = value.rstrip()

    d = dict(
        command  = req.command,
        version  = req.protocol_version,
        origin   = req.client_address,
        url      = req.path,
        path     = url.path,
        params   = url.params,
        query    = url.query,
        fragment = url.fragment,
        headers  = headers,
        postdata = req.postdata
    )
    body = json.dumps(d, indent=2) + '\n'
    body_bytes = body.encode('utf-8')

    req.send_response(200)
    req.send_header('Content-Type', 'application/json')
    req.send_header('Content-Length', str(len(body_bytes)))
    req.end_headers()
    return io.BytesIO(body_bytes)
