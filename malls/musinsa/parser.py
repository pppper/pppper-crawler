import time
from bs4 import BeautifulSoup
import regex
from selectolax.parser import HTMLParser

def extract_musinsa_product_title(bs):
    '''product 명을 반환'''
    name_el = bs.css_first(
        "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em").text()
    return name_el
def extract_musinsa_product_price(bs):
    '''무신사 기준 회원가 중 비회원가 반환, pppper판매가, integer'''
    price = bs.css_first(".txt_price_member").text()
    price = int(price.replace('\n', '').replace('원', '').replace(',', ''))
    return price
def extract_musinsa_product_category(bs):
    '''무신사 기준 최하위 카테고리 반환'''
    category = bs.css_first(".item_categories").text()
    category = category.split(">")[-1].split("\n")[0].replace(" ", "")
    # ">"를 기준으로 분리하고 마지막 원소에서 최하위 카테고리 추출
    return category
def extract_musinsa_product_image(bs):
    '''대표 이미지, 무신사 기준 상세페이지 이미지란의 첫 이미지 주소 반환'''
    image_url = f'https:{bs.css_first(".product-img > img").attrs["src"]}'
    return image_url
def extract_musinsa_product_brand(bs):
    '''브랜드 명, 영문 대문자 띄어쓰기x'''
    brand = bs.css_first(
        ".product_article_contents > strong > a").text().replace(" ", "")
    return brand
def extract_musinsa_product_competitor_price(bs):
    '''무신사 기준 판매가, 할인 전 가격, pppper정상가, integer'''
    competitor_price = bs.css_first(".product_article_price").text()
    competitor_price = int(competitor_price.replace(
        " ", "").replace("원", "").replace(",", ""))
    return competitor_price
def extract_musinsa_product_size_array(bs):
    '''사이즈 배열 반환, 옵션이 여러개일 경우 Assertion Error 던짐'''
    sizes = []
    s = bs.css(".option_cont > select")
    # 옵션 개수를 카운트 했을 때, 그 길이가 1이 아니라면 assertion error 던짐
    assert len(s) == 1 or len(s)==2, "option error"
    box= bs.css_first("#size_table")
    if (box):
        box = box.css("tbody > tr > th")
        for size in box:
            if("MY" not in size.text()):
                sizes.append(size.text())
        if(len(s)==2):
            count = 0
            test = s[0].css("select > option")
            for t in test:
                if("옵션선택" not in t.text().replace(" ","")): count+=1
            assert count==1
            
    else:#사이즈 테이블이 없을 때
    
        if(len(s)==2):
            count = 0
            test = s[0].css("select > option")
            for t in test:
                if("옵션선택" not in t.text().replace(" ","")): count+=1
            assert count==1
            ns = s[1].css("select > option")
            for size in ns:
                size = size.text().replace(" ","").replace("\n","")
                if(size != "옵션선택" and "품절" not in size):
                    # if(size.find("(")!=-1):
                    #     size = size[:size.find("(")]
                    # 옵션선택이거나 품절이 포함되지 않은 경우만 배열에 추가
                    sizes.append(size)
        else:
            ns = bs.css(".option_cont > select > option")    
            for size in ns:
                size = size.text().replace(" ","").replace("\n","")
                if(size != "옵션선택" and "품절" not in size):
                    # if(size.find("(")!=-1):
                    #     size = size[:size.find("(")]
                    # 옵션선택이거나 품절이 포함되지 않은 경우만 배열에 추가
                    sizes.append(size)
    return sizes
def extract_musinsa_product_detail_images(bs):
    '''무신사 기준 상세 이미지 주소 배열 반환'''
    details=bs.css_first("#detail_view").css("img")
    urls=[]
    for detail in details:
        if(".jpg" in detail.attrs["src"]):
            urls.append(detail.attrs["src"])
    return urls
def extract_musinsa_product_banner_images(bs):
    '''무신사 기준 banner 이미지, 주소 배열 반환'''
    start = time.time()
    banners = bs.css("#detail_thumb > ul > li > img")
    banner_urls = []
    for banner in banners:
        banner = banner.attrs["src"]
        if (".jpg" in banner):
            # 배너 그대로 추출할 경우 width가 60인 파일이 추출되기 때문에 width가 500인 주소로 변환
            banner = f'https:{banner.replace("60.jpg", "500.jpg")}'
            banner_urls.append(banner)
    return banner_urls
def extract_musinsa_product_tag_list(bs):
    '''무신사태그+성별+브랜드+카테고리 배열 반환'''
    atags = bs.css("li.article-tag-list > p.product_article_contents > a")
    gender = bs.css_first(".txt_gender > span").text()
    brand = extract_musinsa_product_brand(bs)
    category = extract_musinsa_product_category(bs)
    tags = []
    for tag in atags:
        tags.append(tag.text()[1:])  # 제거
    tags.append(gender)
    tags.append(brand)
    tags.append(category)
    return tags

def parse_product_html(pid, html):
    product = {}
    tree = HTMLParser(html)
    try:
        product['size_array'] = extract_musinsa_product_size_array(tree)
        product['id'] = pid
        product['price'] = extract_musinsa_product_price(tree)
        product['title'] = extract_musinsa_product_title(tree)
        product['video_link'] = None
        product['category'] = extract_musinsa_product_category(tree)
        product['description'] = None
        product['image'] = extract_musinsa_product_image(tree)
        product['brand'] = extract_musinsa_product_brand(tree)
        product['competitor_price'] = extract_musinsa_product_competitor_price(tree)
        product['shipping'] = 0
        product['detail_images'] = extract_musinsa_product_detail_images(tree)
        product['banner_images'] = extract_musinsa_product_banner_images(tree)
        product['item_link']=f'https://store.musinsa.com/app/goods/{pid}'
        product['influencer_show'] = True
        product['style_image'] = extract_musinsa_product_image(tree)
        product['tag_list'] = extract_musinsa_product_tag_list(tree)
        product['item_type'] = "default"
    except AssertionError as e:
        # 사이즈 배열에서 던진 에러 처리, 옵션이 여러개면 파싱을 멈추고 None 반환
        return None
    return product