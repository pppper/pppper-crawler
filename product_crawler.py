import json
import regex
import requests
from utils import jsonprint, timeit
from log import app_logger
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}
# headers = {
#     'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
# }

def crawl_musinsa_product_html(product_id):
    '''product_id를 인자로 받아서 제품 크롤링 및 파싱, JSON 형식으로 반환'''

    # app_logger.debug(f"fetching product html of product id {product_id}")

    url = f'https://store.musinsa.com/app/goods/{product_id}'

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        app_logger.error(f'failed to fetch product html of product id {product_id}', e)

    product_html = response.text
    return product_html
