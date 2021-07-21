import asyncio
import json
import concurrent.futures
from top_brand_crawler import crawl_musinsa_top_brand
from utils import jsonprint
from product_crawler import crawl_musinsa_product_by_id
from brand_product_crawler import crawl_musinsa_brand_products

async def main():
  brands = await crawl_musinsa_top_brand()

  async def crawl_musinsa_products(brand):
    product_ids = crawl_musinsa_brand_products(brand["brandcode"], max_pages=1)
    promises = [crawl_musinsa_product_by_id(product_id) for product_id in product_ids]
    results = await asyncio.gather(*promises, return_exceptions=True)
    name = brand['name']
    result =[]
    #product가 없는 경우는 배제하고 있는 경우에만 리스트에 추가
    for r in results:
      if r!=None:
        result.append(r)
    # print(f'brand: {name} result: {len(result)}')
    return {brand["brandcode"]:result}

  test = [crawl_musinsa_products(brand) for brand in brands ][:50]
  test_result = await asyncio.gather(*test, return_exceptions=True)
  test_results =[]
  for r in test_result:
    test_results.append(r)
  jsonprint(test_results)
asyncio.run(main())