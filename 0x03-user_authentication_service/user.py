#!/usr/bin/env python3
"""User module
"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import INTEGER, VARCHAR, Column


Base = declarative_base()


class User(Base):
    """User model class
    """
    __tablename__ = 'users'

    id = Column(INTEGER, primary_key=True)
    email = Column(VARCHAR(250), nullable=False)
    hashed_password = Column(VARCHAR(250), nullable=False)
    session_id = Column(VARCHAR(250), nullable=True)
    reset_token = Column(VARCHAR(250), nullable=True)


if __name__ == '__main__':
    print(User.__tablename__)

    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
