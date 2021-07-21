from utils import jsonprint
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}

async def extract_musinsa_brand_rank(bs):
  brands=bs.select(".li_inner")
  brand_ranking = []
  for brand in brands:
    brand_rank = brand.select_one("p.txt_num_rank").text.replace(" ","").replace("\n","")
    temp_index = brand_rank.find("위")
    brand_rank = int(brand_rank[:temp_index])
    brand_name = brand.select_one("p.brand_name").text.replace('\n',"")
    brand_code = brand.select_one("p.brand_name_en").text.replace('\n','')
    brand_ranking.append({'rank':brand_rank,'name':brand_name,'brandcode':brand_code})  
  return brand_ranking

async def crawl_musinsa_top_brand():
  async with aiohttp.ClientSession() as session:
    url = 'https://search.musinsa.com/ranking/brand'
    async with session.get(url, headers=headers) as response:
      html = await response.text()
      bs = BeautifulSoup(html, 'html.parser')
      brand_ranking = await extract_musinsa_brand_rank(bs)
      print(brand_ranking)
  return brand_ranking

brands = asyncio.run(crawl_musinsa_top_brand())
# print(brands)
jsonprint(brands)