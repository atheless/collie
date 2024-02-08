"""
Views.
"""

from async_lru import alru_cache

from api.serializers import UserSerializer
from api.viewsets import BaseModelView
from security.models import User
from responses import Response, HTMLResponse, JSONResponse
from settings import templates


async def home_handler(request, **kwargs):
    context = {"title": "Homepage", "user": request.user, "request": request}
    template = templates.get_template('home.html')
    return HTMLResponse(body=template.render(context))


async def about_handler(request, **kwargs):
    context = {"title": "About Page", "user": request.user, "request": request}
    template = templates.get_template('home.html')
    return HTMLResponse(body=template.render(context))


async def some_handler(request, **kwargs):
    pk = kwargs.get('pk')
    return Response(body=f"Received pk {pk}")


class UserModelView(BaseModelView):
    model = User
    serializer_class = UserSerializer

    @alru_cache(ttl=100)
    async def cache_list(self):
        instances = self.session.query(self.model).all()
        serializer = self.serializer_class(many=True)
        data = serializer.dump(instances)
        return data

    async def list(self, request, **kwargs):
        data = await self.cache_list()
        return JSONResponse(indent=4, dict=data)

    async def retrieve(self, request, **kwargs):
        instance = self.session.query(self.model).filter_by(id=kwargs['pk']).first()
        serializer = self.serializer_class()
        data = serializer.dump(instance)
        return JSONResponse(indent=4, dict=data)
