import asyncio
from utils import jsonprint
from product_crawler import crawl_musinsa_product_by_id
from brand_product_crawler import crawl_musinsa_brand_products



async def main():
  product_ids = crawl_musinsa_brand_products("covernat", max_pages=1)
  promises = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids]
  result = await asyncio.gather(*promises, return_exceptions=True)

  results = []
  for r in result:
    if type(r) != AssertionError:
      results.append(r)
  jsonprint(results)


asyncio.run(main())