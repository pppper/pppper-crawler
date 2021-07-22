import json
import regex
import requests
from utils import jsonprint, timeit
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}
# headers = {
#     'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 11_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1"
# }


async def crawl_musinsa_product_html(product_id):
    '''product_id를 인자로 받아서 제품 크롤링 및 파싱, JSON 형식으로 반환'''
    # product = {}
    # 비동기 요청
    # async with aiohttp.ClientSession() as session:
    #   url = f'https://store.musinsa.com/app/goods/{product_id}'
    #   async with session.get(url, headers=headers) as response:
    #     product_html = await response.text()#응답 텍스트 html에 저장
    url = f'https://store.musinsa.com/app/goods/{product_id}'
    response = requests.get(url, headers=headers)
    product_html = response.text

    # print(f"end crawling {product_id}")
    # 파싱 데이터를 JSON 형식으로 저장 및 반환
    return product_html

def crawl_musinsa_product_html2(product_id):
    '''product_id를 인자로 받아서 제품 크롤링 및 파싱, JSON 형식으로 반환'''
    # product = {}
    # 비동기 요청
    # async with aiohttp.ClientSession() as session:
    #   url = f'https://store.musinsa.com/app/goods/{product_id}'
    #   async with session.get(url, headers=headers) as response:
    #     product_html = await response.text()#응답 텍스트 html에 저장
    url = f'https://store.musinsa.com/app/goods/{product_id}'
    response = requests.get(url, headers=headers)
    product_html = response.text

    # print(f"end crawling {product_id}")
    # 파싱 데이터를 JSON 형식으로 저장 및 반환
    return product_html
# product = asyncio.run(crawl_musinsa_product_by_id('1891162'))
# print(product)
# print(json.dumps(product, indent=2, ensure_ascii=False))
