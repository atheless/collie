"""
Test factory.
"""

from datetime import datetime, timedelta

from faker import Faker

from security.basic.authentication import hash_password
from security.models import User, Session, CSRFToken
from settings import rdatabase
import views

def printAll():
    session = rdatabase.get_session()

    print("Users:")
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Password: {user.password}")

    print("\nSessions:")
    sessionsList = session.query(Session).all()
    for s in sessionsList:
        print(f"ID: {s.id}, User ID: {s.user_id}, Session Token: {s.session_token}")

    print("\nCSRF Tokens:")
    csrf_tokens = session.query(CSRFToken).all()
    for token in csrf_tokens:
        print(f"ID: {token.id}, Session ID: {token.session_id}, Token: {token.token}")

    session.close()


def particularPrint():
    session = rdatabase.get_session()

    users = session.query(User).all()

    for user in users:
        print(f"User ID: {user.id}, Username: {user.username}, Password: {user.password}, Email: {user.email}")
        print("Sessions:")
        for user_session in user.sessions:
            print(f" - Session ID: {user_session.id}, Session Token: {user_session.session_token}")
            print("   CSRF Tokens:")
            for csrf_token in user_session.csrf_tokens:
                print(f"    - CSRF Token ID: {csrf_token.id}, CSRF Token: {csrf_token.token}")
        print("--------------")

    print("\n ------CSRF TABLE ------")
    ct = session.query(CSRFToken).all()
    for x in ct:
        print(f'{x.token} {x.session}')

    session.close()



def populate_tables(session, num_users=5):
    fake = Faker()

    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            password=hash_password('123'),
            email=fake.email()
        )
        session.add(user)

        session_obj = Session(
            user=user,
            session_token=fake.uuid4(),
            expiration=datetime.utcnow() + timedelta(days=30)
        )
        session.add(session_obj)

        csrf_token = CSRFToken(token=fake.uuid4(), session=session_obj)
        session.add(csrf_token)

    session.commit()
