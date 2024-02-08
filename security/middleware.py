from security.models import Session
from requests import Request


async def auth_middleware(scope, receive, send):
    from app import app

    if scope['type'] == 'http':
        request = Request(scope, {})
        session_id = request.session_id
        if session_id:
            # Retrieve session from the database
            session = app.db.query(Session).filter(Session.session_token == session_id).first()

            if session:
                # csrf_token = request.headers.get('X-CSRF-Token', None)
                #
                # if csrf_token:
                #     # Check if the CSRF token exists for the session
                #     csrf_token_db = app.db.query(CSRFToken).filter(CSRFToken.session_id == session.id).first()
                #
                #     if csrf_token_db and csrf_token_db.token == csrf_token:
                #         # If both session and CSRF token are valid, allow the request to proceed
                #         scope['user'] = session.user
                #         return await app.handle_request(scope, receive, send)
                scope['user'] = session.user
                return await app.handle_request(scope, receive, send)
    scope['user'] = 'Guest'
    return await app.handle_request(scope, receive, send)
