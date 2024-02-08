from functools import wraps


def query_cache(maxsize=300, ttl=60):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, request, **kwargs):
            key = f"{func.__name__}:{self.model.__name__}"
            cached_result = self._cached_query.get(key)
            if cached_result:
                return cached_result

            result = await func(self, request, **kwargs)
            self._cached_query[key] = result
            return result

        return wrapper

    return decorator


