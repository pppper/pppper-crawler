from unicodedata import category
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}

# response = requests.get('https://store.musinsa.com/app/goods/1876370', headers=headers)
async def crawl_musinsa_product_title(bs):
  name_el = bs.select_one("#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em")
  return {"title": name_el.text}
async def crawl_musinsa_product_price(bs):
  price = bs.find("span", {"class":"txt_price_member m_list_price"}).text           
  price = int(price.replace('\n','').replace('원','').replace(',',''))
  return {"price": price}
async def crawl_musinsa_product_category(bs):
  category = bs.select_one(".item_categories")
  category=category.text.split(">")[-1].split("\n")[0].replace(" ","")
  return {"category": category}

async def crawl_musinsa_product_async(product_id):
  async with aiohttp.ClientSession() as session:
    async with session.get(f'https://store.musinsa.com/app/goods/{product_id}', headers=headers) as response:
      html = await response.text()
      bs = BeautifulSoup(html, 'html.parser')
      crawled_data=[]
      crawled_data.append(await crawl_musinsa_product_title(bs))
      crawled_data.append(await crawl_musinsa_product_price(bs))
      crawled_data.append(await crawl_musinsa_product_category(bs))
  return crawled_data

# def crawl_musinsa_product_name(product_id):
#   response = requests.get(f'https://store.musinsa.com/app/goods/{product_id}', headers=headers)
#   html = response.text
#   bs = BeautifulSoup(html, 'html.parser')
#   name_el = bs.select_one("#size_table")
#   params = (
#     ('type', 'detail'),
#   )
  
#   response_price = requests.get(f'https://store.musinsa.com/app/svc/member_price_new/{product_id}/0', headers=headers, params=params)
#   html_price = response_price.text

#   ps = BeautifulSoup(html_price,'html.parser')
#   price_el = ps.select_one(".txt_price_member")
#   price = int(price_el.text.replace(',', '')[:-1])

#   return name_el, price

name_el = asyncio.run(crawl_musinsa_product_async('419333'))
print(name_el)
