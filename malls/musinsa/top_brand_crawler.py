from utils import jsonprint
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}

async def extract_musinsa_brand_rank(bs):
  '''브랜드 정보를 JSON 형식으로 반환 {rank: integer, name: str, brandcode: str}'''
  #탑 100 브랜드를 brands에 저장
  brands=bs.select(".li_inner")
  brand_ranking = []
  for brand in brands:
    #각 브랜드의 순위, 이름, 브랜드코드를 JSON으로 반환
    brand_rank = brand.select_one("p.txt_num_rank").text.replace(" ","").replace("\n","")
    temp_index = brand_rank.find("위")
    #"위"를 기준으로 뒤의 배열은 다 날림, (순위 변동도 날림)
    brand_rank = int(brand_rank[:temp_index])
    brand_name = brand.select_one("p.brand_name").text.replace('\n',"")
    brand_code = brand.select_one("p.brand_name_en").text.replace('\n','')
    brand_ranking.append({'rank':brand_rank,'name':brand_name,'brandcode':brand_code})  
  return brand_ranking

async def crawl_musinsa_top_brand():
  '''무신사 브랜드 랭킹 TOP100 브랜드 JSON 반환'''
  async with aiohttp.ClientSession() as session:
    url = 'https://search.musinsa.com/ranking/brand'
    async with session.get(url, headers=headers) as response:
      html = await response.text()
      bs = BeautifulSoup(html, 'html.parser')
      brand_ranking = await extract_musinsa_brand_rank(bs)
  return brand_ranking

brands = asyncio.run(crawl_musinsa_top_brand())
# print(brands)
jsonprint(brands)