from mini_amazon import app
from flask import request,render_template, Response
from mini_amazon.models.product import Product

prod = Product()


@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/api/products', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        query=request.args['name']

        matches = prod.search_by_name(query)
        output_type = request.args.get('output_type',None)
        if output_type == 'html':
            return render_template('results.html',query=query,results=matches)
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
