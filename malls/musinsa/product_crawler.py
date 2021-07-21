import json
import regex
from utils import jsonprint
from bs4 import BeautifulSoup
import asyncio
import aiohttp

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
}

async def extract_musinsa_product_title(bs):
  '''product 명을 반환'''
  name_el = bs.select_one("#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em")
  return name_el.text
async def extract_musinsa_product_price(bs):
  '''무신사 기준 회원가 중 비회원가 반환, pppper판매가, integer'''
  price = bs.find("span", {"class":"txt_price_member m_list_price"}).text           
  price = int(price.replace('\n','').replace('원','').replace(',',''))
  return price
async def extract_musinsa_product_category(bs):
  '''무신사 기준 최하위 카테고리 반환'''
  category = bs.select_one(".item_categories")
  category=category.text.split(">")[-1].split("\n")[0].replace(" ","")
  # ">"를 기준으로 분리하고 마지막 원소에서 최하위 카테고리 추출
  return category
async def extract_musinsa_product_image(bs):
  '''대표 이미지, 무신사 기준 상세페이지 이미지란의 첫 이미지 주소 반환'''
  image_url = f'https:{bs.select_one(".product-img > img").get("src")}'
  return image_url
async def extract_musinsa_product_brand(bs):
  '''브랜드 명, 영문 대문자 띄어쓰기x'''
  brand=bs.select_one(".product_article_contents > strong > a").text.replace(" ","")
  return brand
async def extract_musinsa_product_competitor_price(bs):
  '''무신사 기준 판매가, 할인 전 가격, pppper정상가, integer'''
  competitor_price = bs.select_one(".product_article_price").text
  competitor_price=int(competitor_price.replace(" ","").replace("원","").replace(",",""))
  return competitor_price
async def extract_musinsa_product_size_array(bs):
  '''사이즈 배열 반환, 옵션이 여러개일 경우 Assertion Error 던짐'''
  sizes=[]
  s = bs.select(".option_cont > select")
  #옵션 개수를 카운트 했을 때, 그 길이가 1이 아니라면 assertion error 던짐
  assert len(s) == 1
  ns = bs.select(".option_cont > select > option")
  for size in ns:
    size=size.text.replace(" ","").replace("\n","")
    if(size!="옵션선택" and "(품절)" not in size):
      #옵션선택이거나 품절이 포함되지 않은 경우만 배열에 추가
      sizes.append(size)
  return sizes
async def extract_musinsa_product_detail_images(bs):
  '''무신사 기준 상세 이미지 주소 배열 반환'''
  #정규표현식 이용해서 이미지 주소 추출
  pattern = regex.compile('(?<=<img alt=".+?" src=").+?(?=")')
  urls = pattern.findall(str(bs.select_one('#detail_view')))
  for url in urls:
    #움짤, gif 인 경우, urls 배열에서 제거
    if (".gif" in url):
      urls.remove(url)
  return urls
async def extract_musinsa_product_banner_images(bs):
  '''무신사 기준 banner 이미지, 주소 배열 반환'''
  banners = bs.select(".product_thumb > li > img")
  banner_urls=[]
  for banner in banners:
      banner = banner.get("src")
      if (".jpg" in banner):
        #배너 그대로 추출할 경우 width가 60인 파일이 추출되기 때문에 width가 500인 주소로 변환 
        banner=f'https:{banner.replace("60.jpg", "500.jpg")}'
        banner_urls.append(banner)
  return banner_urls
async def extract_musinsa_product_tag_list(bs):
  '''무신사태그+성별+브랜드+카테고리 배열 반환'''
  atags = bs.select("li.article-tag-list > p.product_article_contents > a")
  gender = bs.select_one(".txt_gender > span").text
  brand = await extract_musinsa_product_brand(bs)
  category = await extract_musinsa_product_category(bs)
  tags=[]
  for tag in atags:
    tags.append(tag.text[1:])# #제거
  tags.append(gender)
  tags.append(brand)
  tags.append(category)
  return tags
async def crawl_musinsa_product_by_id(product_id):
  '''product_id를 인자로 받아서 제품 크롤링 및 파싱, JSON 형식으로 반환'''
  print(f"start crawling {product_id}")
  #비동기 요청
  async with aiohttp.ClientSession() as session:
    url = f'https://store.musinsa.com/app/goods/{product_id}'
    async with session.get(url, headers=headers) as response:
      html = await response.text()#응답 텍스트 html에 저장
      bs = BeautifulSoup(html, 'html.parser')#파싱 준비
      product={}
      product['id'] = product_id
      product['title']=await extract_musinsa_product_title(bs)
      product['price']=await extract_musinsa_product_price(bs)
      product['video_link']=None
      product['category']=await extract_musinsa_product_category(bs)
      product['description']=None
      product['image']=await extract_musinsa_product_image(bs)
      product['brand']=await extract_musinsa_product_brand(bs)
      product['competitor_price']=await extract_musinsa_product_competitor_price(bs)
      product['shipping']=0
      product['size_array']=await extract_musinsa_product_size_array(bs)
      product['detail_images']=await extract_musinsa_product_detail_images(bs)
      product['banner_images']=await extract_musinsa_product_banner_images(bs)
      product['item_link']=url
      product['influencer_show']=True
      product['styled_image']=await extract_musinsa_product_image(bs)
      product['tag_list']=await extract_musinsa_product_tag_list(bs)
      product['item_type']="default"
  print(f"end crawling {product_id}")
  #파싱 데이터를 JSON 형식으로 저장 및 반환
  return product

# product = asyncio.run(crawl_musinsa_product_by_id('1891162'))
# print(product)
# print(json.dumps(product, indent=2, ensure_ascii=False))
