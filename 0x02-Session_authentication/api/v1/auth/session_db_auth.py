#!/usr/bin/env python3
""" Module of a Session Authentication with Expiry class
"""
from typing import TypeVar
from datetime import datetime, timedelta
import uuid
from os import getenv
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ Session authentication & expiry with DB manager class
    """
    def create_session(self, user_id=None):
        """ Create a session id associated with a user id and create time
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        SessionDBAuth.user_id_by_session_id[session_id] = UserSession(
            user_id=user_id, session_id=session_id
        )
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve a session id associated with a user id before duration
        """
        user_id = super().user_id_for_session_id(session_id)
