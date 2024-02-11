from typing import Dict, Any, Callable

from database.relational_dbs import Database
from requests import Request
from security.authentication import SessionManager
from security.middleware import auth_middleware
from settings import rdatabase, ACCESS_CONTROL_ALLOW_ORIGIN, DEBUG


class Application:
    def __init__(self, session_manager: SessionManager, rdb: Database):
        self.db = rdb.get_session()
        self.session_manager = session_manager

    @staticmethod
    async def handle_request(scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        from urls import router

        if scope['type'] == 'http':
            path = scope['path']
            data = dict(await receive())
            request = Request(scope, data)
            request.user = scope['user']
            response = await router.route_request(path=path, method=scope['method'], request=request)
            headers = *[
                (b'content-type', response.content_type),
                *response.response_header,
                (b'Access-Control-Allow-Origin', ', '.join(ACCESS_CONTROL_ALLOW_ORIGIN).encode()),
                (b'Access-Control-Allow-Methods', ', '.join(response.ACCESS_CONTROL_ALLOW_METHODS).encode()),
                (b'Access-Control-Allow-Headers', ', '.join(response.ACCESS_CONTROL_ALLOW_HEADERS).encode()),
            ],
            await send({'type': 'http.response.start',
                        'status': response.status_code,
                        'headers': headers,
                        })
            await send({'type': 'http.response.body', 'body': response.body.encode(), })

    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        if scope['type'] == 'http':
            await auth_middleware(scope, receive, send)


app = Application(session_manager=SessionManager(), rdb=rdatabase)
# Define routes for routing.


# if DEBUG:
    # populate_tables(app.db, num_users=1)
    # Debug Print tables
    # printAll()
