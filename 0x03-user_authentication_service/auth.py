#!/usr/bin/env python3
"""Auth module
"""
from typing import Union
import bcrypt
import base64 as b64
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash the input password with some salt
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a stringified uuid
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialise the member 'DB' instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with an email + password
        """
        try:
            duplicate_user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(
                email,
                b64.b64encode(_hash_password(password)).decode())

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login info is valid
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode(),
                b64.b64decode(user.hashed_password.encode()))
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Create a new session for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get the user associated with a specific session_id
        """
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroy the session for the specific user
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Create a password reset token
        """
        user = self._db.find_user_by(email=email)
        if user is None:
            raise ValueError
        reset_token = _generate_uuid()
        user.reset_token = reset_token
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password
        """
        user = self._db.find_user_by(reset_token=reset_token)
        if user is None:
            raise ValueError
        user.hashed_password = b64.b64encode(_hash_password(password))
        user.reset_token = None


if __name__ == '__main__':
    # print(_hash_password("Hello Holberton"))

    # email = 'me@me.com'
    # password = 'mySecuredPwd'

    # auth = Auth()

    # try:
    #     user = auth.register_user(email, password)
    #     print("successfully created a new user!")
    # except ValueError as err:
    #     print("could not create a new user: {}".format(err))

    # try:
    #     user = auth.register_user(email, password)
    #     print("successfully created a new user!")
    # except ValueError as err:
    #     print("could not create a new user: {}".format(err))

    ####################################################################

    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth = Auth()

    auth.register_user(email, password)

    print(auth.valid_login(email, password))

    print(auth.valid_login(email, "WrongPwd"))

    print(auth.valid_login("unknown@email", password))

    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth = Auth()

    auth.register_user(email, password)

    print(auth.create_session(email))
    print(auth.create_session("unknown@email.com"))
