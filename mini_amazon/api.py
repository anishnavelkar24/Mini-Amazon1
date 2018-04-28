from mini_amazon import app
from flask import request,render_template, send_from_directory,Response
from mini_amazon.models.product import ProductModel
from mini_amazon.models.user import UserModel

prod = ProductModel()
user_model=UserModel()

@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        query=request.args['name']
        user_id = request.args['user_id']

        matches = prod.search_by_name(query)
        output_type = request.args.get('output_type',None)
        if output_type == 'html':
            return render_template('results.html',query=query,results=matches, user_id = user_id)
        else:

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

@app.route('/api/users', methods=['POST'])
def user():
    if request.form['op_type'] == 'login':
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        is_valid = user_model.authenticate(username, password)
        if is_valid:
            user_data = user_model.get_user_by_username(username)
            return render_template('profile.html',
                                   name=user_data['name'],
                                   user_id=user_data['_id'])
        else:
            return render_template('index.html', login_msg='Invalid username/password')
    if request.form['op_type'] == 'signup':
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        # TODO : validation
        is_valid = True

        if is_valid:
            user_model.add_new_user(name, email, username, password)
            user_data = user_model.get_by_username(username)
            return render_template('profile.html',
                                   name=name,
                                   user_id=user_data['_id'])
        else:
            return render_template('index.html', signup_msg='User name already exists')
    else:
        status = {
            'status': 'Invalid op_type'
        }
        return Response(str(status), status=400, mimetype='application/json')

@app.route('/api/cart', methods=['POST'])
def cart():
    user_id = request.form.get('user_id', None)
    product_id = request.form.get('product_id', None)
    print (user_id)
    success = user_model.add_product_to_cart(user_id, product_id)

        # irrespective of success
    user_data = user_model.get_by_id(user_id)
    return render_template('profile.html',
                            name=user_data['name'],
                            user_id=user_data['_id'])