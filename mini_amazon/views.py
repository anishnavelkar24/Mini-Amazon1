from flask import send_from_directory
from mini_amazon import app


@app.route('/', methods=['GET'])
def index():
    return send_from_directory('./mini_amazon/static', 'index.html')
