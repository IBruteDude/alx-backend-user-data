#!/usr/bin/env python3
"""Integration endpoint testing module
"""
import requests as rs


def register_user(email: str, password: str) -> None:
    """Test the user registeration endpoint
    """
    response = rs.post("http://localhost:5000/users",
                       data={'email': email, 'password': password})
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test the user wrong login endpoint
    """
    response = rs.post("http://localhost:5000/sessions",
                       data={'email': email, 'password': password})
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test the user correct login endpoint
    """
    response = rs.post("http://localhost:5000/sessions",
                       data={'email': email, 'password': password})
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get('session_id')


def profile_unlogged() -> None:
    """Test the user profile endpoint without login
    """
    response = rs.get("http://localhost:5000/profile")
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test the user profile endpoint with login
    """
    response = rs.get("http://localhost:5000/profile",
                      cookies={'session_id': session_id})
    assert 'email' in response.json()


def log_out(session_id: str) -> None:
    """Test the user logout endpoint
    """
    response = rs.delete("http://localhost:5000/sessions",
                         cookies={'session_id': session_id})
    assert response.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    """Test the password reset endpoint
    """
    response = rs.post("http://localhost:5000/reset_password",
                       data={'email': email})
    assert response.json()['email'] == email
    assert "reset_token" in response.json()
    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test the password update endpoint
    """
    response = rs.put("http://localhost:5000/reset_password",
                      data={'email': email,
                            'reset_token': reset_token,
                            'new_password': new_password})
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
