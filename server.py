import io
from image_processing import remove_background
from index import getDb
from flask.json import jsonify
from musinsa.index import crawl_product
from flask import Flask, send_file, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return "api enterance"


@app.route("/api/v1/crawl-product/<product_id>")
def get_product(product_id):
    '''제품 1개 크롤링(데이터베이스 저장은x)'''
    product = crawl_product(product_id)
    if product:
        # getDb()['products'].replace_one({'_id': product_id}, product, upsert=True)
        return jsonify(product)
    else:
        return 'parsing failed', 404


@app.route("/api/v1/crawl-products", methods=['POST'])
def crawl_products():
    '''제품 1개 크롤링(데이터베이스 저장o)'''
    pass


@app.route("/api/v1/remove-background", methods=['GET'])
def request_remove_background():
    image_url = request.args.get("imageUrl")
    image = remove_background(image_url)
    img_io = io.BytesIO()
    image.save(img_io, 'png')
    img_io.seek(0)
    return send_file(img_io, mimetype="image/jpeg")