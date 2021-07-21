import json
import regex
from utils import jsonprint, timeit, timeit_async
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}


  
async def crawl_musinsa_product_by_id(product_id):
  start = time.time()
  print(f"start crawling {product_id}")
  async with aiohttp.ClientSession() as session:
    url = f'https://store.musinsa.com/app/goods/{product_id}'
    async with session.get(url, headers=headers) as response:
      html = await response.text()
      product = html
      # bs = BeautifulSoup(html, 'html.parser')
      # product={}
      # product['id'] = product_id
      # product['title']=await extract_musinsa_product_title(bs)
      # product['price']=await extract_musinsa_product_price(bs)
      # product['video_link']=None
      # product['category']=await extract_musinsa_product_category(bs)
      # product['description']=None
      # product['image']=await extract_musinsa_product_image(bs)
      # product['brand']=await extract_musinsa_product_brand(bs)
      # product['competitor_price']=await extract_musinsa_product_competitor_price(bs)
      # product['shipping']=0
      # product['size_array']=await extract_musinsa_product_size_array(bs)
      # product['detail_images']=await extract_musinsa_product_detail_images(bs)
      # product['banner_images']=await extract_musinsa_product_banner_images(bs)
      # product['item_link']=url
      # product['influencer_show']=True
      # product['styled_image']=await extract_musinsa_product_image(bs)
      # product['tag_list']=await extract_musinsa_product_tag_list(bs)
      # product['item_type']="default"
  end = time.time()
  print(f"end crawling {product_id}, elapsed time: {end-start}")
  return product

# product = asyncio.run(crawl_musinsa_product_by_id('1891162'))
# print(product)
# print(json.dumps(product, indent=2, ensure_ascii=False))
