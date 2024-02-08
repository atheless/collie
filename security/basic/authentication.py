import hmac
from datetime import datetime, timedelta
from urllib.parse import parse_qs
from uuid import uuid4

from security.models import User, Session
from responses import Response, Redirect, HTMLResponse
from settings import templates, SECRET


def hash_password(password):
    # Hash the password securely
    salt = SECRET.encode()
    return hmac.new(salt, password.encode('utf-8'), 'sha256').hexdigest()


def compare_hashed_passwords(hashed_password, password):
    # Use hmac.compare_digest for constant-time comparison
    return hmac.compare_digest(hashed_password.encode('utf-8'), hash_password(password).encode('utf-8'))


async def basic_auth_handler(request, **kwargs):
    from app import app
    data = parse_qs(request.body.decode('utf-8'))
    if data:
        username = data.get('username')[0]
        password = data.get('password')[0]
        # Check if user exists in the database
        user = app.db.query(User).filter(User.username == username).first()

        if user and compare_hashed_passwords(hashed_password=user.password, password=password):
            expiration = datetime.utcnow() + timedelta(days=1)  # Set expiration date/time
            # Create session
            session_id = str(uuid4())
            session = Session(user_id=user.id, session_token=session_id, expiration=expiration)
            app.db.add(session)
            app.db.commit()

            # # Generate CSRF token
            # csrf_token = str(uuid4())
            # csrf_token_entry = CSRFToken(session_id=session.id, token=csrf_token)
            # app.db.add(csrf_token_entry)
            # app.db.commit()

            # Set session_id cookie
            response_headers = [(b'Set-Cookie',
                                 f'session_id={session_id}; Expires={expiration.strftime("%a, %d %b %Y %H:%M:%S GMT")}'.encode())]
            return Response(body=f"Login successful. Welcome, {username}!", content_type=b'text/html',
                            headers=response_headers)
        else:
            kwargs['context'] = {'result_auth': 'Invalid username or password.'}
            return await loginPage(request, **kwargs)
            # return Redirect(body="Invalid username or password.", location='/login', context='Invalid username or password.')
    return Response(body="Only POST request is accepted", content_type=b'text/html')


async def logout_handler(request, **kwargs):
    from app import app
    session_id = request.session_id
    if session_id:
        # Delete session from the database
        session = app.db.query(Session).filter(Session.session_token == session_id).first()
        if session:
            app.db.delete(session)
            app.db.commit()
            # Remove session_id cookie to logout user
            response_headers = [(b'Set-Cookie', b'session_id=; Expires=Thu, 01 Jan 1969 00:00:00 GMT')]
            return Redirect(body="Logout successful.", location='/login', headers=response_headers)
    return Redirect(body="No active session found.", location='/', headers='')


async def loginPage(request, **kwargs):
    # csrf_token = str(uuid4())
    context = {"title": "Login Page", "user": request.user, **kwargs.get('context', {})}
    template = templates.get_template('login.html')
    return HTMLResponse(body=template.render(context))
    # csrf_token = CSRFToken(token=csrf_token)
    # from app import app
    # app.db.add(csrf_token)
    # app.db.commit()
    # response_headers = [(b'Set-Cookie', f'csrf_token={csrf_token}; Secure; HttpOnly'.encode())]
    # return Response(body=response_body, content_type=b'text/html', headers=response_headers)
