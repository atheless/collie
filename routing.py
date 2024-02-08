from typing import Callable, Dict, Any, Tuple

from requests import Request
from responses import Response


class Router:
    def __init__(self):
        self.routes: Dict[str, Dict[str, Callable]] = {}

    def add_route(self, path: str, method: str, handler: Callable):
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    # async def get_handler(self, path: str, method: str) -> tuple[Callable[..., Any], str] | tuple[
    #     Callable[..., Any], None] | None:
    #     for route, methods in self.routes.items():
    #         if '<pk>' in route:
    #             if route.split('<pk>')[0] in path and method in methods:  # route.split('/')[1] in path
    #                 pk = path.split('/')[-1]
    #                 return methods[method], pk
    #         elif route == path and method in methods:
    #             return methods[method], ['None']
    #     return None, None

    async def get_handler(self, path: str, method: str) -> (Callable[..., Any] | None, str | None):
        for route, methods in self.routes.items():
            if '<pk>' in route:
                route_parts = route.split('<pk>')
                route_prefix = route_parts[0]
                if route_prefix in path and method in methods:
                    pk_index = path.find(route_prefix) + len(route_prefix)
                    pk = path[pk_index:].split('/')[0]
                    return methods[method], pk
            elif route == path and method in methods:
                return methods[method], None
        return None, None

    async def route_request(self, path: str, method: str, request: Request, **kwargs):
        handler, kwargs['pk'] = await self.get_handler(path, method)
        if handler:
            return await handler(request, **kwargs)
        return Response(body="404 Not Found!", status_code=404)


