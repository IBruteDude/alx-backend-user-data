#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")  # , echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._save()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        """
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        """
        user: User = self.find_user_by(id=user_id)
        for name, value in kwargs.items():
            setattr(user, name, value)
        self._save()

    def _save(self):
        """
        """
        self._session.commit()
        # self._session.flush()


if __name__ == '__main__':
    my_db = DB()

    # user_1 = my_db.add_user("test@test.com", "SuperHashedPwd")
    # print(user_1.id)

    # user_2 = my_db.add_user("test1@test.com", "SuperHashedPwd1")
    # print(user_2.id)

    ########################################################################

    # user = my_db.add_user("test@test.com", "PwdHashed")
    # print(user.id)

    # find_user = my_db.find_user_by(email="test@test.com")
    # print(find_user.id)

    # try:
    #     find_user = my_db.find_user_by(email="test2@test.com")
    #     print(find_user.id)
    # except NoResultFound:
    #     print("Not found")

    # try:
    #     find_user = my_db.find_user_by(no_email="test@test.com")
    #     print(find_user.id)
    # except InvalidRequestError:
    #     print("Invalid")

    ########################################################################

    # email = 'test@test.com'
    # hashed_password = "hashedPwd"

    # user = my_db.add_user(email, hashed_password)
    # print(user.id)

    # try:
    #     my_db.update_user(user.id, hashed_password='NewPwd')
    #     print("Password updated")
    # except ValueError:
    #     print("Error")

    ########################################################################
