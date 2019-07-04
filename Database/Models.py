# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, text, Boolean, CHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    pk = Column(Integer, nullable=False)
    username = Column(String(50), nullable=False)
    follower_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    password = Column(String(50), nullable=False)
    profile_url = Column(String(255), nullable=False)
    delete = Column(CHAR(1), nullable=False)

    def __init__(self, pk, username, follower_count, following_count, password, profile_url):
        self.pk = pk
        self.username = username
        self.follower_count = follower_count
        self.following_count = following_count
        self.password = password
        self.profile_url = profile_url
        self.delete = ''

    def __repr__(self):
        return "<User(id='%s', pk='%s', username='%s', follower_count='%s', following_count='%s', profile_url='%s')>" % (
            self.id, self.pk, self.username, self.follower_count, self.following_count, self.profile_url)


class Follower(Base):
    __tablename__ = 'followers'

    pk = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    profile_url = Column(String(250), nullable=False)
    following_count = Column(Integer, nullable=False)
    follower_count = Column(Integer, nullable=False)
    is_private = Column(Boolean, nullable=False)
    status_refresh = Column(Boolean, nullable=False)
    users_id = Column(ForeignKey('users.id'), nullable=False)
    delete = Column(CHAR(1), nullable=False)

    users = relationship('User')

    def __init__(self, pk, username, profile_url, following_count, follower_count, is_private, status_refresh, users_id):
        self.pk = pk
        self.username = username
        self.profile_url = profile_url
        self.following_count = following_count
        self.follower_count = follower_count
        self.is_private = is_private
        self.status_refresh = status_refresh
        self.users_id = users_id
        self.delete = ''

    def __repr__(self):
        return "<User(id='%d', pk='%d', username='%s', profile_url='%s', following_count='%d', follower_count='%d'," \
               "is_private='%s', status_refresh='%s', users_id='%d')>" % (self.id, self.pk, self.username,
                                                                          self.profile_url, self.following_count,
                                                                          self.follower_count, self.is_private,
                                                                          self.status_refresh, self.users_id)


class Following(Base):
    __tablename__ = 'followings'

    pk = Column(Integer, nullable=False)
    follower_count = Column(Integer, nullable=False)
    following_count = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    is_private = Column(Boolean, nullable=False)
    profile_url = Column(String(250), nullable=False)
    status_refresh = Column(Boolean, nullable=False)
    users_id = Column(ForeignKey('users.id'), nullable=False)
    delete = Column(CHAR(1), nullable=False)

    users = relationship('User')

    def __init__(self, pk, username, profile_url, following_count, follower_count, is_private, status_refresh, users_id):
        self.pk = pk
        self.username = username
        self.profile_url = profile_url
        self.following_count = following_count
        self.follower_count = follower_count
        self.is_private = is_private
        self.status_refresh = status_refresh
        self.users_id = users_id
        self.delete = ''

    def __repr__(self):
        return "<User(id='%d', pk='%d', username='%s', profile_url='%s', following_count='%d', follower_count='%d'," \
               "is_private='%s', status_refresh='%s', users_id='%d')>" % (self.id, self.pk, self.username,
                                                                          self.profile_url, self.following_count,
                                                                          self.follower_count, self.is_private,
                                                                          self.status_refresh, self.users_id)
