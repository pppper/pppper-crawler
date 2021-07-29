from index import getDb
from flask.json import jsonify
from product_parser import parse_product_html
from product_crawler import crawl_musinsa_product_html
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "hello world"

@app.route("/api/v1/crawl-product/<product_id>")
def crawl_product(product_id):
    '''제품 1개 크롤링(데이터베이스 저장은x)'''
    html = crawl_musinsa_product_html(product_id)
    product = parse_product_html(product_id, html)
    if product:
        # getDb()['products'].replace_one({'_id': product_id}, product, upsert=True)
        return jsonify(product)
    else:
        return 'parsing failed', 404

@app.route("/api/v1/crawl-products", methods=['POST'])
def crawl_products():
    '''제품 1개 크롤링(데이터베이스 저장o)'''
    pass
