from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref)
from sqlalchemy.ext.declarative import declarative_base

# from model import Household as HouseholdModel, Family_Member as Family_MemberModel


engine = create_engine('sqlite:///database.sqlite3') 
db_session = scoped_session(sessionmaker(autocommit=False,
                                            autoflush=False,
                                            bind=engine))

Base = declarative_base() # table creation
Base.query = db_session.query_property() # query execution


class Item(Base):
    __tablename__ = 'item'
    item_id = Column(String(256), primary_key=True)
    item_name = Column(String(256))
    item_price = Column(String(256))



