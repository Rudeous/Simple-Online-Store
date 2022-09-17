import os
from flask import Flask, render_template, request, jsonify, json, redirect, url_for
from flask_graphql import GraphQLView
import requests
from helper import *
import logging
# from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

logging.basicConfig(filename='controller.log', level=logging.DEBUG)

# graphql_URL = "http://127.0.0.1:5001/graphql" # local
graphql_URL = "http://gql_app:5001/graphql" # docker
# CORS(app)

@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def index():
    # call graphql server to get data
    gql_items_response = requests.get(graphql_URL+'?query=query{allItems{edges{node{itemId itemName itemPrice}}}}')
    gql_items_json = gql_items_response.json()
    return render_template('index.html.j2', items=gql_items_json['data']['allItems']['edges'])

@app.route('/create_item', methods=['POST', 'GET'])
def create_item():
    if request.method == 'GET':
        return render_template('create_item.html.j2')
    if request.method == 'POST':
        # backend logic to create item
        # data = request.args
        # print(data)
        # new_itemName = data['item_name']
        # new_itemPrice = data['item_price']

        # frontend logic to create item
        new_itemName = request.form['item_name']
        new_itemPrice = request.form['item_price']

        gql_items_response = requests.get(graphql_URL+'?query=query{allItems{edges{node{itemId itemPrice itemName}}}}')
        gql_items_json = gql_items_response.json()
        print(gql_items_json)
        item_sort_list = []
        for item in gql_items_json['data']['allItems']['edges']:
            item["node"]["itemId"] = int(item["node"]["itemId"]) # convert itemId to int
            item_sort_list.append(item["node"]) # append item to list

        # sort list of item objects by itemId
        item_sort_list.sort(key=lambda x: x["itemId"]) 

        # after ordering by itemId in asc order, retrieve the last itemId
        largest_itemId = item_sort_list[-1]["itemId"]

        # increment the largest itemId by 1 to get the new itemId to be created
        new_itemId = str(largest_itemId + 1)

        item_post_url = graphql_URL +  '?query=mutation{createItem' + \
            f'(itemId:"{new_itemId}",itemName:"{new_itemName}", itemPrice:"{new_itemPrice}")' + \
            '{item{itemId itemName itemPrice}}}'
        print(item_post_url)
        item_post_response = requests.post(item_post_url)
        print(item_post_response)
        return redirect(url_for('index'))



# @app.route('/read_all_items', methods=['GET'])
# def read_all_items():
#     # retrieve arguments to retrieve from request
#     args = request.args

#     # build url to query graphql server for item with fields specified
#     gql_items_response = requests.get(graphql_URL+'?query=query{allItems{edges{node'+generate_family_member_url(args)+'}}}')
#     gql_items_json = gql_items_response.json()
#     return json.dumps(gql_items_json, indent=4), gql_items_response.status_code

@app.route('/update_item', methods=['POST'])
def update_item():
    # args = request.args # search by itemId since to get a one item
    # convert args to mutable dict
    # item_id = args['item_id']
    # item_name = args['item_name']
    # item_price = args['item_price']

    # frontend logic to update item
    print(request.form)
    item_id = request.args.get('item_id')
    new_itemName = request.form['item_name']
    new_itemPrice = request.form['item_price']



    url = graphql_URL + '?query=mutation{updateItem' + \
        f'(itemId:"{item_id}",itemName:"{new_itemName}", itemPrice:"{new_itemPrice}")' + \
        '{item{itemId itemName itemPrice}}}'
    print(url)
    update_item_response = requests.post(url)
    update_item_json = update_item_response.json()
    print(update_item_json)
    return redirect(url_for('index'))

@app.route('/delete_item', methods=['POST'])
def delete_item():
    args = request.args
    item_id = args['item_id']
    # item_id = request.form['item_id']
    url = graphql_URL + '?query=mutation{deleteItem' + \
        f'(itemId:"{item_id}")' + \
        '{item{itemId itemName itemPrice}}}'
    print(url)
    delete_item_response = requests.post(url)
    delete_item_json = delete_item_response.json()
    print(delete_item_json)
    return redirect(url_for('index'))

# sets up logging
@app.route('/logs')
def logs():
    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("Warning log info")
    app.logger.error("Error log info")
    app.logger.critical("Critical log info")
    return "testing logging levels."


if __name__ == "__main__":
    # run seed data script to populate database with seed data
    app.run(port=5002, debug=False, host='0.0.0.0')

