from flask import Flask, send_from_directory, request, Response
from product import Product

app = Flask('mini-amazon', static_url_path='')
#login_manager = LoginManager()

prod = Product()

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        matches = prod.search_by_name(request.args['name'])
        return Response(str(matches),mimetype='application/json',status=200)

    elif request.method == 'POST':
        if request.form['op_type']=="insert":
            product = dict()
            product['name'] = request.form['name']
            product['description'] = request.form['description']
            product['price'] = request.form['price']
            prod.save(product)
            return Response(str({'status':'success'}),mimetype='application/json',status= 200)
        elif request.form['op_type']=="delete":
            _id = request.form['_id']
            prod.delete_by_id(_id)
            return Response(str({'status': 'success'}), mimetype='application/json', status=200)
        elif request.form['op_type'] == "update":
            _id = request.form['_id']
            updated_product = dict()

            if request.form['name']!='':
                updated_product['name'] = request.form['name']
            if request.form['description']!='':
                updated_product['desc'] = request.form['description']
            if request.form['price']!='':
                updated_product['price'] = request.form['price']
                prod.update_by_id(_id,updated_product)
            return Response(str({'status':'updated'}),mimetype='application/json',status=200)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)
   # login_manager.init_app(app)
