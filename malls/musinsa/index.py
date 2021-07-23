from top_brand_crawler import crawl_musinsa_top_brand
import asyncio
from parser import parse_product_html
from tqdm import tqdm
# import json
# import time
import concurrent.futures
from product_crawler import crawl_musinsa_product_html2
from brand_product_crawler import crawl_musinsa_brand_products

from pymongo import MongoClient
mongodb_URI = "mongodb://sotalabs:sotalabs1!@localhost:27017"
client = MongoClient(mongodb_URI)

product_collection = client['crawler']['products']


def fetch_product_htmls(brand, max_products=100):
    max_pages = max_products // 90 + 1
    # crawl brand product ids
    pids = crawl_musinsa_brand_products(
        brand, max_pages=max_pages)[:max_products-1]

    # crawl each product html by id
    htmls = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=90) as executor:
        bar = tqdm(executor.map(
            crawl_musinsa_product_html2, pids), total=len(pids))
        bar.set_description(f"crawling {brand} products:")
        for pid, html in zip(pids, bar):
            htmls[pid] = html

    return htmls


def parse_product_htmls(brand, htmls):
    products = {}
    bar = tqdm(htmls)
    bar.set_description(f"parsing {brand} products:")
    count = 0
    errors = []
    for pid in bar:
        html = htmls[pid]
        product = parse_product_html(pid, html)
        # print(html)
        if product:
            products[pid] = product
            count += 1
        else:
            errors.append(pid)
    print('brand coverage: ', 100 * (count / len(htmls)), '%')
    # print('errors', errors)

    return products
    # 하루에 상위 50개 브랜드, 브랜드당 200개 -> 10000개 제품


# brands = asyncio.run(crawl_musinsa_top_brand())[:10]
# brands = [brand['brandcode'] for brand in brands]
brands = ['archivepke','alphaindustries','badblood','bensimon','branded','blond9','bemusemansion','covernat','converse','drmartens','espionage','etmon','ebbetsfield','ept','fcmm','fatalism','halbkreis','insilencewomen','kirsh','lafudgeforwomen','lafudgestore','leire','lee','lmc','mardimercredi','marithefrancoisgirbaud','markgonzales','mahagrid','maisonmined','modnine','mixxo','millioncor','nationalgeographic','neikidnis','outdoorproducts','outstanding','oioi','partimento','rothco','sovermentwithlomort','suare','spao','signature','thisisneverthat','takeasy','toffee','travel','uniformbridge','vivastudio','viaplain','wvproject','xero','yale','yourlifehere']
print(len(brands))
for brand in brands:
    htmls = fetch_product_htmls(brand, 91)
    # print(htmls)
    products = parse_product_htmls(brand, htmls)

    for pid in products:
        product = products[pid]
        product = {'_id': pid, **product}
        product_collection.replace_one({'_id': pid}, product, upsert=True)
