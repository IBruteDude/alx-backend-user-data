#!/usr/bin/env python3
""" Module for the password encryptor
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Hash a password argument and salt it
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Check if a hashed password matchs the original one
    """
    return bcrypt.checkpw(password.encode(), hashed_password)


if __name__ == '__main__':
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))

    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
