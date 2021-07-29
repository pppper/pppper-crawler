from musinsa.product_parser import parse_product_html
from tqdm import tqdm
from time import sleep
import concurrent.futures
from musinsa.product_crawler import fetch_product_html
from musinsa.brand_product_crawler import crawl_musinsa_brand_product_ids
import numpy as np

from log import app_logger


from pymongo import MongoClient


def getDb():
    mongodb_URI = "mongodb://sotalabs:sotalabs1!@localhost:27017"
    client = MongoClient(mongodb_URI)
    db = client['crawler']
    return db


def fetch_product_htmls(brand, max_products=200):
    max_pages = max_products // 90 + 1
    # crawl brand product ids
    app_logger.debug(
        f"crawl product htmls of brand <{brand}>, {max_pages} pages, {max_products} products each")
    product_ids = crawl_musinsa_brand_product_ids(
        brand, max_pages=max_pages)[:max_products-1]
    app_logger.debug(
        f"completed product htmls of brand <{brand}>, {max_products} products each finished: {len(product_ids)} products are crawled")

    # crawl each product html by id
    htmls = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=90) as executor:
        app_logger.debug(f"start fetching <{brand}> products")
        for pid, html in zip(product_ids, executor.map(
                fetch_product_html, product_ids)):
            htmls[pid] = html
        app_logger.debug(f"complete fetching <{brand}> products html")

    return htmls


def parse_product_htmls(brand, htmls):
    products = {}
    count = 0
    parse_failed_product_ids = []

    app_logger.debug(
        f"parse product htmls for brand <{brand}> ({len(htmls)} products)")
    for pid in htmls:
        html = htmls[pid]
        product = parse_product_html(pid, html)
        if product:
            products[pid] = product
            count += 1
        else:
            parse_failed_product_ids.append(pid)
            # app_logger.warning(f"parsing failed for product <{pid}>")
    app_logger.critical(
        f'brand <{brand}> coverage: {100 * (count / len(htmls))}%')

    return products
    # 하루에 상위 50개 브랜드, 브랜드당 200개 -> 10000개 제품


# brands = asyncio.run(crawl_musinsa_top_brand())[:10]
# brands = [brand['brandcode'] for brand in brands]
brands = ['archivepke', 'alphaindustries', 'badblood', 'bensimon', 'branded', 'blond9', 'bemusemansion', 'covernat', 'converse', 'drmartens', 'espionage', 'etmon', 'ebbetsfield', 'ept', 'fcmm', 'fatalism', 'halbkreis', 'insilencewomen', 'kirsh', 'lafudgeforwomen', 'lafudgestore', 'leire', 'lee', 'lmc', 'mardimercredi', 'marithefrancoisgirbaud', 'markgonzales',
          'mahagrid', 'maisonmined', 'modnine', 'mixxo', 'millioncor', 'nationalgeographic', 'neikidnis', 'outdoorproducts', 'outstanding', 'oioi', '5252byoioi', 'partimento', 'rothco', 'sovermentwithlomort', 'suare', 'spao', 'signature', 'thisisneverthat', 'takeasy', 'toffee', 'travel', 'uniformbridge', 'vivastudio', 'viaplain', 'wvproject', 'xero', 'yale', 'yourlifehere']
# print(len(brands))


def crawl_brand(brand):
    app_logger.info(f"[brand] start crawling brand <{brand}>")
    htmls = fetch_product_htmls(brand, 200)
    products = parse_product_htmls(brand, htmls)

    # app_logger.debug(f"[brand] start crawling brand <{brand}>")
    for pid in products:
        product = products[pid]
        product = {'_id': pid, **product}
        getDb()['products'].replace_one({'_id': pid}, product, upsert=True)


def crawl(brands):
    app_logger.info(f"start crawling brands <{brands}>")
    STAGE_SIZE = 15  # split brands into array of arrays(max 20 size)

    app_logger.debug(f"splitting brands into brand_groups")
    split_points = [i * STAGE_SIZE for i in range(len(brands) // STAGE_SIZE)]

    completed_brands = []

    if len(brands) < STAGE_SIZE:
        brand_groups = np.array([brands])
    else:
        brand_groups = np.split(
            np.array(brands), indices_or_sections=split_points[1:])
    # app_logger.debug(f"brand_groups: {brand_groups}")

    for i in range(len(brand_groups)):
        brand_group = brand_groups[i]
        # app_logger.debug(f"crawling brand group ({i} / {len(brand_groups)})")
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            for brand, data in zip(brands, executor.map(crawl_brand, brand_group)):
                completed_brands.append(brand)
                app_logger.info(
                    f"completed crawling brand <{brand}> ({len(completed_brands)}/{len(brands)})")
                pass
        sleep_time = 60 * 3
        app_logger.info(f"sleeping {sleep_time}s...")
        sleep(sleep_time)
        app_logger.info('resuming...')


if __name__ == '__main__':
    crawl(brands)
