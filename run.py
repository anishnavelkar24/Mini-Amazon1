from flask import Flask, send_from_directory, request, Response
import pymongo
from pymongo import MongoClient
import re
client=MongoClient('localhost',27017)
db=client.tvb_amazon

app = Flask('mini-amazon', static_url_path='')

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method=='GET':
        query= {
            'name': re.compile(request.args['name'],re.IGNORECASE)

            }

        matching_prods=db.products.find(query)
        matches=[]
        for prod in matching_prods:
            matches.append(prod)

        return Response(str(matches),mimetype='application/json',status=200)

    elif request.method == 'POST':
        if request.form['op_type']=="insert":
            product = dict()
            product['name'] = request.form['name']
            product['description'] = request.form['description']
            product['price'] = request.form['price']
            db.products.insert_one(product)
            return Response(str({'status':'success'}),mimetype='application/json',status= 200)
        elif request.form['op_type']=="delete":
            name = request.form['name']
            db.products.delete_one(filter={'name':name})
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)
        elif request.form['op_type'] == "update":
            condition = dict()
            condition['name'] = request.form['cur_name']

            replacement=dict()
            if request.form['name']!='':
                replacement['name'] = request.form['name']
            if request.form['description']!='':
                replacement['desc'] = request.form['description']
            if request.form['price']!='':
                replacement['price'] = request.form['price']
            db.products.update_one(filter=condition, update={'$set':replacement})
            return Response(str({'status':'updated'}),mimetype='application/json',status=200)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
