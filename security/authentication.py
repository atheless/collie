from typing import Dict


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, str]] = {}

    def create_session(self, username: str, expiration: str):
        session_id = username
        self.sessions[session_id] = {'username': username, 'expiration': expiration}

    def validate_session(self, session_id: str) -> bool:
        if session_id in self.sessions:
            return True
        return False

    def get_username(self, session_id: str) -> str:
        return self.sessions[session_id]['username']