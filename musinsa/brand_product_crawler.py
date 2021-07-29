from types import coroutine
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from pprint import pprint

import time
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
}

def crawl_musinsa_brand_product_ids(brand_code, max_pages=10):
    '''브랜드 페이지에서 product_id 배열 반환
    페이지당 최대 90개 크롤링 가능'''
    # print(f"start crawling {brand_code}")
    def crawl_page(page):
        '''페이지 기준 product_id 배열 반환'''
        params = (
            ('sortCode', '1m'),
            ('page', page),
            ('size', 90),
            ('listViewType', 'small'),
        )

        response = requests.get(f'https://display.musinsa.com/display/brands/{brand_code}', headers=headers, params=params)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        elements = soup.select("#searchList > li")
        product_ids = []

        for element in elements:
            #각 상품에서 id 추출, 저장
            product_id = int(element.select_one("a[name='goods_link']")['href'].split('/')[-1])
            product_ids.append(product_id)
        return product_ids

    product_id_dict = {}#페이지 별로 product id 저장하기 위한 딕셔너리
    
    #멀티쓰레딩, 쓰레드풀, 비동기로 할일 할당
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #crawl_page함수를 비동기로 호출, 쓰레드 최대 10개, {future 객체:page}를 future_to_page에 저장
        future_to_page = {executor.submit(crawl_page, page): page for page in range(1, max_pages + 1)}
        #future_to_page에서 완료된 값을 product_id_dict에 저장
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            product_id_dict[page] = future.result()
            
    product_ids = []
    
    #페이지 순서대로 배열에 다시 저장
    for page in range(1, max_pages + 1):
        product_ids += product_id_dict[page]
    #product id 배열 반환
    return product_ids
    

        
# res = crawl_musinsa_brand_products("grooverhyme", max_pages=10)