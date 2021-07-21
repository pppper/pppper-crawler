import asyncio
from parser import parse_product
import time
from utils import jsonprint
from product_crawler import crawl_musinsa_product_by_id
from brand_product_crawler import crawl_musinsa_brand_products

async def main():
  start = time.time()
  product_ids = crawl_musinsa_brand_products("covernat", max_pages=1)
  promises = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids]

  result = await asyncio.gather(*promises, return_exceptions=True)
  for r in result:
    print(await parse_product(r))

  end = time.time()
  time_elapsed = end - start
  print(time_elapsed)


asyncio.run(main())