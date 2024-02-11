from abc import ABC, abstractmethod


from app import app

from responses import Response


class APIView(ABC):
    def __init__(self, request, **kwargs):
        self.request = request

    async def __call__(self, request, **kwargs):
        return await self.dispatch(**kwargs)

    async def dispatch(self, **kwargs):
        method = self.request.method.upper()
        if method == 'GET':
            return await self.get(**kwargs)
        elif method == 'POST':
            return await self.post(**kwargs)
        elif method == 'PUT':
            return await self.put(**kwargs)
        elif method == 'DELETE':
            return await self.delete(**kwargs)
        elif method == 'PATCH':
            return await self.patch(**kwargs)
        else:
            return Response(status_code=405, body="Method Not Allowed")

    @abstractmethod
    async def get(self, **kwargs):
        pass

    @abstractmethod
    async def post(self, **kwargs):
        pass

    @abstractmethod
    async def put(self, **kwargs):
        pass

    @abstractmethod
    async def delete(self, **kwargs):
        pass

    @abstractmethod
    async def patch(self, **kwargs):
        pass


class BaseModelView:
    model = None
    serializer_class = None
    relational_database = app.db
    ACCESS_CONTROL_ALLOW_METHODS = ['*']
    ACCESS_CONTROL_ALLOW_HEADERS = ['Content-Type']

    def __init__(self):
        self.session = BaseModelView.relational_database

    async def __call__(self, request, **kwargs):
        return await self.dispatch(request, **kwargs)

    async def dispatch(self, request, **kwargs):

        method = request.method
        if method not in self.ACCESS_CONTROL_ALLOW_METHODS and not '*':
            return Response(status_code=405, body="Method Not Allowed")
        if method == 'GET':
            if kwargs['pk']:
                return await self.retrieve(request, **kwargs)
            else:
                return await self.list(request, **kwargs)
        elif method == 'POST':
            return await self.create(request, **kwargs)
        elif method == 'PUT' and kwargs['pk']:
            return await self.update(request, **kwargs)
        elif method == 'DELETE' and kwargs['pk']:
            return await self.destroy(request, **kwargs)

        return Response(status_code=405, body="Method Not Allowed")

    async def get_object(self, **kwargs):
        pass

    async def list(self, request, **kwargs):
        pass

    async def create(self, data):
        pass

    async def retrieve(self, **kwargs):
        pass

    async def update(self, **kwargs):
        pass

    async def destroy(self, **kwargs):
        pass

    def serializer(self, data):
        if self.serializer_class:
            serializer = self.serializer_class(many=True)
            if serializer.is_valid(data):
                return serializer.dump(data)
            else:
                return {'error': 'Invalid data.'}

        return {'error': 'Serializer was not defined.'}

    @classmethod
    def as_view(cls):
        return cls()



