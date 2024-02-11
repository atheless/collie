import json
from enum import Enum


class ContentType(Enum):
    TEXT_PLAIN = b'text/plain'
    TEXT_HTML = b'text/html'
    APPLICATION_JSON = b'application/json'


class Response:
    def __init__(self, *, body: str, status_code: int = 200, content_type: str = b"text/plain", headers=''):
        self.body = body
        self.status_code = status_code
        self.content_type = content_type
        self.response_header = headers
        self.ACCESS_CONTROL_ALLOW_METHODS = ['*']
        self.ACCESS_CONTROL_ALLOW_HEADERS = ['Content-Type']

    async def encode(self):
        return self.body.encode()


class HTMLResponse(Response):
    def __init__(self, *, body: str, status_code: int = 200, headers=''):
        super().__init__(body=body, status_code=status_code, content_type=b'text/html', headers=headers)


class JSONResponse(Response):
    def __init__(self, *, indent: int = 2, dict: str, status_code: int = 200, headers=''):
        super().__init__(body=json.dumps(dict, indent=indent), status_code=status_code,
                         content_type=b'application/json', headers=headers)


class Redirect(Response):
    def __init__(self, body, location: str, status_code: int = 302, headers='', context: str = ''):
        super().__init__(body=body, status_code=302, headers=headers)
        self.response_header = [(b'Location', location.encode())]
        if headers:
            self.response_header.append(*headers)
        self.body = f"Redirecting to {location}"

