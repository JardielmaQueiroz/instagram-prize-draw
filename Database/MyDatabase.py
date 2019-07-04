import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .Models import Base


class MyDatabase:

    def __init__(self):
        self.session = None
        self.db_name = 'db.sqlite3'
        self.db_engine = create_engine('sqlite:///'+self.db_name)
        self.create_database()

    def getSession(self):
        if self.session == None:
            session_maker = sessionmaker(bind=self.db_engine)
            self.session = session_maker()
        return self.session

    def create_database(self):
        if self.db_name not in os.listdir():
            Base.metadata.create_all(self.db_engine)
