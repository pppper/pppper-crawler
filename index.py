import asyncio
from concurrent.futures.process import ProcessPoolExecutor
from parser import parse_product
import time
from utils import jsonprint
from product_crawler import crawl_musinsa_product_by_id
from brand_product_crawler import crawl_musinsa_brand_products
from functools import wraps

async def main():
  start = time.time()
  product_ids = crawl_musinsa_brand_products("covernat", max_pages=1)
  promises = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids]

  product_htmls = await asyncio.gather(*promises, return_exceptions=True)

  fetch_end = time.time()
  with ProcessPoolExecutor(max_workers=20) as executor:
    # for max_workers -> 8 , 32.84 seconds / 4 , 
    for product_html, product in zip(product_htmls, executor.map(parse_product, product_htmls)):
      print('completed parsing', product['title'])

  all_end = time.time()
  time_elapsed = all_end - start
  print(f'''
  fetch time: {fetch_end - start}
  parse time: {all_end - fetch_end}
  total: {all_end - start}
  ''')


asyncio.run(main())