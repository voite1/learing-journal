import datetime

from cryptacular.pbkdf2 import PBKDF2PasswordManager as Manager

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    DateTime,
    UnicodeText,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(length=255), nullable=False, unique=True)
    body = Column(Unicode, nullable=True, default=u'')
    created = Column(DateTime, default=datetime.datetime.now)
    edited = Column(DateTime, default=datetime.datetime.now)
    
    @classmethod
    def all(cls):
        """return a query with all entries, ordered by creation date reversed
        """
        return DBSession.query(cls).order_by(cls.created).all()

    @classmethod
    def by_id(cls, id):
        """return a single entry identified by id
        If no entry exists with the provided id, return None
        """
        return DBSession.query(cls).get(id)

class User(Base):
    __tablename__ = 'user'
    id=Column(Integer, primary_key=True)
    name=Column(Unicode(length=255), nullable=False, unique=True)
    password=Column(Unicode, nullable=False)

    def verify_password(self, password):
        manager = Manager()
        return manager.check(self.password, password)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()

