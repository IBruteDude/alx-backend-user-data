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
    def create_session(self, user_id=None) -> str:
        """ Create a session id associated with a user id and create time
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        UserSession(user_id=user_id, session_id=session_id).save()
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """ Retrieve a session id associated with a user id before duration
        """
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return None
        return user_sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """ Destroy the session/Log out the current user
        Return:
            - True on successful logout
            - False on error
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if len(user_sessions) == 0:
            return False
        user_sessions[0].remove()
        return True
