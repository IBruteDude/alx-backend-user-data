#!/usr/bin/env python3
""" Module of a Basic Authentication class
"""
from typing import Tuple, TypeVar
from api.v1.views.users import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication manager class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """ Get the auth header base64 encoded part
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if authorization_header[:6] != 'Basic ':
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """ Get the decoded base64 encoded auth header part
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) is not str:
            return None

        from base64 import decodebytes
        try:
            return decodebytes(base64_authorization_header.encode()).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """ Extract the user email and password from header
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if decoded_base64_authorization_header.find(':') == -1:
            return None, None

        user_email_pwd = decoded_base64_authorization_header.split(':')
        return (user_email_pwd[0], ':'.join(user_email_pwd[1:]))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """ Create a User instance with specified credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if type(user_email) is not str or type(user_pwd) is not str:
            return None
        users = User.search({'email': user_email})
        if len(users) < 1:
            return None
        if not users[0].is_valid_password(user_pwd):
            return None
        return users[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user authorized for a request
        """
        if request is None:
            return None
        auth_header = self.authorization_header(request)
        b64_header = self.extract_base64_authorization_header(auth_header)
        header_data = self.decode_base64_authorization_header(b64_header)
        user_email, user_pwd = self.extract_user_credentials(header_data)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user


if __name__ == '__main__':
    a = BasicAuth()

    print(a.extract_base64_authorization_header(None))
    print(a.extract_base64_authorization_header(89))
    print(a.extract_base64_authorization_header("Holberton School"))
    print(a.extract_base64_authorization_header("Basic Holberton"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    print(a.extract_base64_authorization_header(
        "Basic SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.extract_base64_authorization_header("Basic1234"))

    print(a.decode_base64_authorization_header(None))
    print(a.decode_base64_authorization_header(89))
    print(a.decode_base64_authorization_header("Holberton School"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.decode_base64_authorization_header(
        a.extract_base64_authorization_header(
            "Basic SG9sYmVydG9uIFNjaG9vbA==")))

    print(a.extract_user_credentials(None))
    print(a.extract_user_credentials(89))
    print(a.extract_user_credentials("Holberton School"))
    print(a.extract_user_credentials("Holberton:School"))
    print(a.extract_user_credentials("bob@gmail.com:toto1234"))

    import uuid
    from models.user import User

    """ Create a user test """
    user_email = str(uuid.uuid4())
    user_clear_pwd = str(uuid.uuid4())
    user = User()
    user.email = user_email
    user.first_name = "Bob"
    user.last_name = "Dylan"
    user.password = user_clear_pwd
    print("New user: {}".format(user.display_name()))
    user.save()

    """ Retreive this user via the class BasicAuth """

    a = BasicAuth()

    u = a.user_object_from_credentials(None, None)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(89, 98)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials("email@notfound.com", "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, user_clear_pwd)
    print(u.display_name() if u is not None else "None")

    import base64
    from models.user import User

    """ Create a user test """
    user_email = "bob100@hbtn.io"
    user_clear_pwd = "H0lberton:School:98!"

    user = User()
    user.email = user_email
    user.password = user_clear_pwd
    print("New user: {}".format(user.id))
    user.save()

    basic_clear = "{}:{}".format(user_email, user_clear_pwd)
    print("Basic Base64: {}".format(
        base64.b64encode(basic_clear.encode('utf-8')).decode("utf-8")))
