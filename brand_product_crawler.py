from types import coroutine
import concurrent.futures
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36',
}

def crawl_musinsa_brand_products(brand_code, max_pages=10):
    '''total: 10pages'''
    def crawl_page(page):
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
            product_id = int(element.select_one("a[name='goods_link']")['href'].split('/')[-1])
            product_ids.append(product_id)

        return product_ids

    product_id_dict = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_page = {executor.submit(crawl_page, page): page for page in range(1, max_pages + 1)}
        for future in concurrent.futures.as_completed(future_to_page):
            page = future_to_page[future]
            product_id_dict[page] = future.result()
            
    product_ids = []
    
    for page in range(1, max_pages + 1):
        product_ids += product_id_dict[page]
    return product_ids
    

        
# res = crawl_musinsa_brand_products("grooverhyme", max_pages=10)