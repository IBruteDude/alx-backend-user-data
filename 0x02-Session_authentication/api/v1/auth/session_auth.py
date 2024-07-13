#!/usr/bin/env python3
""" Module of a Session Authentication class
"""
from typing import TypeVar
import uuid
from api.v1.auth.auth import Auth
from api.v1.views.users import User


class SessionAuth(Auth):
    """ Session authentication manager class
    """
    user_id_by_session_id = {}
    def create_session(self, user_id: str = None) -> str:
        """ Create a session id associated with a user id
        """
        if user_id is None or type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Retrieve a session id associated with a user id
        """
        if session_id is None or type(session_id) is not str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        if user_id is None:
            return None
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """ Destroy the session/Log out the current user
        Return:
            - True on successful logout
            - False on error
        """
        if request is None:
            return False
        session_id =  self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
        

if __name__ == '__main__':
    sa = SessionAuth()

    print("{}: {}".format(type(sa.user_id_by_session_id), sa.user_id_by_session_id))

    user_id = None
    session = sa.create_session(user_id)
    print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

    user_id = 89
    session = sa.create_session(user_id)
    print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

    user_id = "abcde"
    session = sa.create_session(user_id)
    print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

    user_id = "fghij"
    session = sa.create_session(user_id)
    print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

    user_id = "abcde"
    session = sa.create_session(user_id)
    print("{} => {}: {}".format(user_id, session, sa.user_id_by_session_id))

    ###################################

    user_id_1 = "abcde"
    session_1 = sa.create_session(user_id_1)
    print("{} => {}: {}".format(user_id_1, session_1, sa.user_id_by_session_id))

    user_id_2 = "fghij"
    session_2 = sa.create_session(user_id_2)
    print("{} => {}: {}".format(user_id_2, session_2, sa.user_id_by_session_id))

    print("---")

    tmp_session_id = None
    tmp_user_id = sa.user_id_for_session_id(tmp_session_id)
    print("{} => {}".format(tmp_session_id, tmp_user_id))

    tmp_session_id = 89
    tmp_user_id = sa.user_id_for_session_id(tmp_session_id)
    print("{} => {}".format(tmp_session_id, tmp_user_id))

    tmp_session_id = "doesntexist"
    tmp_user_id = sa.user_id_for_session_id(tmp_session_id)
    print("{} => {}".format(tmp_session_id, tmp_user_id))

    print("---")

    tmp_session_id = session_1
    tmp_user_id = sa.user_id_for_session_id(tmp_session_id)
    print("{} => {}".format(tmp_session_id, tmp_user_id))

    tmp_session_id = session_2
    tmp_user_id = sa.user_id_for_session_id(tmp_session_id)
    print("{} => {}".format(tmp_session_id, tmp_user_id))

    print("---")

    session_1_bis = sa.create_session(user_id_1)
    print("{} => {}: {}".format(user_id_1, session_1_bis, sa.user_id_by_session_id))

    tmp_user_id = sa.user_id_for_session_id(session_1_bis)
    print("{} => {}".format(session_1_bis, tmp_user_id))

    tmp_user_id = sa.user_id_for_session_id(session_1)
    print("{} => {}".format(session_1, tmp_user_id))
