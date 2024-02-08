class Request:
    def __init__(self, scope, message):
        converted_dict = {key.decode(): value.decode() for key, value in scope['headers']}
        cookie_value = converted_dict.get('cookie', '')
        self.session_id = ''
        if 'session_id=' in cookie_value:
            self.session_id = cookie_value.split('session_id=')[1].split(';')[0]

        self.scope = scope
        self.user = scope.get('user', 'guest')
        self.path = scope['path']
        self.method = scope['method']
        self.headers = dict(scope['headers'])
        self.query_params = self._parse_query_params(scope.get('query_string', b''))
        self.body = message.get('body')

    def _parse_query_params(self, query_string):
        if query_string:
            params = query_string.decode().split('&')
            return {param.split('=')[0]: param.split('=')[1] for param in params}
        else:
            return {}

    def is_user_authenticated(self):
        if self.user != "Guest":
            return True
        return False
