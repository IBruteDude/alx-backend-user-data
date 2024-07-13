#!/usr/bin/env python3
""" Module of a Session Authentication with Expiry class
"""
from datetime import datetime, timedelta
from os import getenv
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Session authentication & expiry manager class
    """
    def __init__(self):
        """ Initialise the instance with a session duration
        """
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session id associated with a user id and create time
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        SessionExpAuth.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a session id associated with a user id before duration
        """
        if session_id is None:
            return None
        session_dict = SessionExpAuth.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if SessionExpAuth.session_duration <= 0:
            return session_dict['user_id']
        if session_dict.get('created_at') is None:
            return None
        if session_dict['created_at'] + timedelta(
            seconds=SessionExpAuth.session_duration
        ) < datetime.now():
            return None
        return session_dict['user_id']
