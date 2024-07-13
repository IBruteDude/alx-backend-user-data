#!/usr/bin/env python3
""" Module of the Base of Authentication mechanisms
"""
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Base authentication manager class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if a path requires authentication
        """
        if path is None or excluded_paths is None:
            return True
        if path in excluded_paths or path + '/' in excluded_paths:
            return False
        for expath in excluded_paths:
            if ((expath.endswith('*') or expath.startswith('*')) and
                    path.find(expath.strip('*')) != -1):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Extract the 'Authorization' header
        """
        if request is None:
            return None
        if request.headers.get('Authorization') is None:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user
        """
        return None

    def session_cookie(self, request=None):
        """ Get the the cookie value of a request
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))


if __name__ == '__main__':
    a = Auth()

    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.authorization_header())
    print(a.current_user())

    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/",
                                           "/api/v1/stats"]))

    from flask import Flask, request

    auth = Auth()

    app = Flask(__name__)

    @app.route('/', methods=['GET'], strict_slashes=False)
    def root_path():
        """ Root path
        """
        return "Cookie value: {}\n".format(auth.session_cookie(request))

    app.run(host="0.0.0.0", port="5000")
