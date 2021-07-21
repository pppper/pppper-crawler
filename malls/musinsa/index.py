import asyncio
from parser import parse_product
import time
from utils import jsonprint
from product_crawler import crawl_musinsa_product_by_id
import math
from brand_product_crawler import crawl_musinsa_brand_products

async def main():
  start = time.time()
  product_ids = crawl_musinsa_brand_products("covernat", max_pages=1)
  promises = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids]
  # epoch = 80
  # for r in range(math.floor(len(product_ids)/epoch)):
  #   promises1 = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids[r*epoch:min(r*epoch+(epoch-1), len(product_ids) - 1)]]
  result = await asyncio.gather(*promises, return_exceptions=True)
  for r in result:
    print(await parse_product(r))
  # print(result)
  # result = await asyncio.gather(*promises, return_exceptions=True)

  end = time.time()
  time_elapsed = end - start
  print(time_elapsed)



  # results = []
  # for r in result:
  #   if type(r) != AssertionError:
  #     results.append(r)
  # jsonprint(results)


asyncio.run(main())