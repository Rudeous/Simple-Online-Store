import graphene
from graphene import relay, Field, String, List
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from model import Item as ItemModel, db_session
# from helper import *



"""
purpose: to convert the SQLAlchemy models to Graphene objects with a graph schema
"""
class Item(SQLAlchemyObjectType):
    class Meta:
        model = ItemModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    # return all entries
    all_items = SQLAlchemyConnectionField(Item.connection)
    
    # return individual entry
    item = Field( Item, item_id=graphene.String() ) # filter family_members by item_id

    # student_bonus = Field(List(Household))

    
    def resolve_item(cls, info, item_id):
        return db_session.query(ItemModel).filter_by(item_id=item_id).first()

    
"""
Mutations
"""
# create a new item entry
class CreateItem(graphene.Mutation):

    class Arguments:
        item_id = graphene.String(required=True)
        item_name = graphene.String()
        item_price = graphene.String()
    item = graphene.Field(lambda: Item)

    def mutate(self, info, item_id, item_name, item_price):
        item = ItemModel(item_id = item_id, item_name=item_name, item_price=item_price)
        db_session.add(item)
        db_session.commit()
        return CreateItem(item=item)

# update an existing item entry
class UpdateItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.String(required=True)
        item_name = graphene.String()
        item_price = graphene.String()
    item = graphene.Field(lambda: Item)

    def mutate(self, info, item_id, item_name, item_price):
        item = db_session.query(ItemModel).filter_by(item_id=item_id).first()
        item.item_name = item_name
        item.item_price = item_price
        db_session.commit()
        return UpdateItem(item=item)

# delete an existing item entry
class DeleteItem(graphene.Mutation):
    class Arguments:
        item_id = graphene.String(required=True)
    item = graphene.Field(lambda: Item)

    def mutate(self, info, item_id):
        item = db_session.query(ItemModel).filter_by(item_id=item_id).first()
        db_session.delete(item)
        db_session.commit()
        return DeleteItem(item=item)

# creates a mutation for the schema
class Mutation(graphene.ObjectType):
    create_item = CreateItem.Field()
    update_item = UpdateItem.Field()
    delete_item = DeleteItem.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Item])