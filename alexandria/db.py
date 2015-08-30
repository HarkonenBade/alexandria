from __future__ import absolute_import, print_function

import contextlib
import random

from sqlalchemy import (Boolean, create_engine, Column,
                        DateTime, ForeignKey, Integer, String)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///alexandria.db', echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    token = Column(String(64))
    name = Column(String, default="unnamed")
    admin = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('user.id'))


class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    person = Column(String)
    submitter = Column(Integer, ForeignKey('user.id'))
    date_added = Column(DateTime)


def new_token():
    return hex(random.getrandbits(40*4))[2:-1]


def check_token(sesh, token, admin):
    try:
        if admin:
            return sesh.query(User).filter(User.token == token,
                                           User.admin == True).one()
        else:
            return sesh.query(User).filter(User.token == token).one()
    except NoResultFound:
        return None


def init_db():
    Base.metadata.create_all(engine)
    print("Setup new db.")
    print("Creating admin user.")
    with session_scope() as sesh:
        u = User()
        u.name = "admin"
        u.admin = True
        u.token = new_token()
        print("Admin token: ", u.token)
        sesh.add(u)
    print("DB setup complete.")


@contextlib.contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def obj_to_dict(obj):
    return {col.name: getattr(obj, col.name) for col in obj.__table__.columns}
