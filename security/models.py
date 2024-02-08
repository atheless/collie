from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BaseModel = declarative_base(metadata=MetaData())


class User(BaseModel):
    __tablename__ = 'users'
    # __table_args__ = {'info': {'exclude_from_migrations': True}}
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)  # Store hashed
    email = Column(String, unique=True)
    sessions = relationship("Session", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"

class Session(BaseModel):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="sessions")
    session_token = Column(String, unique=True)
    csrf_tokens = relationship("CSRFToken", back_populates="session")
    expiration = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
class CSRFToken(BaseModel):
    __tablename__ = 'csrf_tokens'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    session = relationship("Session", back_populates="csrf_tokens")
    token = Column(String, unique=True)

    def __init__(self, token, session=None):  # CSRF tokens for both authenticated and anonymous users
        self.token = token
        self.session = session


# # Password reset table (optional)
# class PasswordResetToken(Base):
#     __tablename__ = 'password_reset_tokens'
#     __table_args__ = {"schema": "exclude_from_migrations"}
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     user = relationship("User")
#     token = Column(String, unique=True)
#     created_at = Column(DateTime, default=datetime.utcnow)


# When a user logs in, you generate a session token, store it in the Session table, and associate it with the user's ID. You also generate a CSRF token and associate it with the session ID in the CsrfToken table.
#
# When handling requests that require authentication, you verify the session token and associated CSRF token to ensure the request is valid and secure against CSRF attacks.