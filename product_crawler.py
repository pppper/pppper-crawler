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
  end = time.time()
  print(f"end crawling {product_id}, elapsed time: {end-start}")
  return product