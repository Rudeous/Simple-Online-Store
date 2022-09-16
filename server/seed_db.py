from model import *
from schema import Query, Mutation, schema
import os
from datetime import datetime, date


# delete db if exists
if os.path.exists('database.sqlite3'):
    db_session.close()
    Base.metadata.drop_all(bind=engine) 
    os.remove('database.sqlite3')

# start db session
conn = db_session.connection()

# create tables in db if not done
Base.metadata.create_all(bind=engine)

# household population
item1 = Item(item_id='1', item_name='yang zhou fried race', item_price='4.50')
item2 = Item(item_id='2', item_name='chicken fried race', item_price='5.50')
item3 = Item(item_id='3', item_name='prawn fried race', item_price='6.50')
item4 = Item(item_id='4', item_name='abalone fried race', item_price='10')
item5 = Item(item_id='5', item_name='salted egg fried race', item_price='8')

# add to db
db_session.add(item1)
db_session.add(item2)
db_session.add(item3)
db_session.add(item4)
db_session.add(item5)


# commit to db
db_session.commit()

