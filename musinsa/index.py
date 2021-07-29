from musinsa.product_crawler import fetch_product_html
from musinsa.product_parser import parse_product_html

def crawl_product(product_id):
    html = fetch_product_html(product_id)
    product = parse_product_html(product_id, html)
    return product