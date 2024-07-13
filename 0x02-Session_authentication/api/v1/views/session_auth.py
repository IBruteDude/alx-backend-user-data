#!/usr/bin/env python3
""" Module of Session auth views
"""
from os import getenv
from flask import request, jsonify, session, abort
from api.v1.views import app_views
from api.v1.views.users import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def authenticate_session() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - User object JSON represented
      - 400 if no email or password is provided
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or len(email) == 0:
        return jsonify({ "error": "email missing" }), 400
    if password is None or len(password) == 0:
        return jsonify({ "error": "password missing" }), 400
    users = User.search({'email': email})
    if len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    if not users[0].is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(users[0].id)
    resp = jsonify(users[0].to_json())
    resp.set_cookie(getenv('SESSION_NAME'), session_id)
    return resp

@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /api/v1/auth_session/logout
    Return:
      - empty JSON if the Session is destroyed successfully
      - 404 if logout failed
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200
