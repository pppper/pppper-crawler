from utils import timeit
from bs4 import BeautifulSoup
import regex

@timeit
def extract_musinsa_product_title(bs):
    name_el = bs.select_one(
        "#page_product_detail > div.right_area.page_detail_product > div.right_contents.section_product_summary > span > em")
    return name_el.text

@timeit
def extract_musinsa_product_price(bs):
    price = bs.find("span", {"class": "txt_price_member m_list_price"}).text
    price = int(price.replace('\n', '').replace('원', '').replace(',', ''))
    return price

@timeit
def extract_musinsa_product_category(bs):
    category = bs.select_one(".item_categories")
    category = category.text.split(">")[-1].split("\n")[0].replace(" ", "")
    return category


@timeit
def extract_musinsa_product_image(bs):
    image_url = f'https:{bs.select_one(".product-img > img").get("src")}'
    return image_url


@timeit
def extract_musinsa_product_brand(bs):
    brand = bs.select_one(
        ".product_article_contents > strong > a").text.replace(" ", "")
    return brand


@timeit
def extract_musinsa_product_competitor_price(bs):
    competitor_price = bs.select_one(".product_article_price").text
    competitor_price = int(competitor_price.replace(
        " ", "").replace("원", "").replace(",", ""))
    return competitor_price


@timeit
def extract_musinsa_product_size_array(bs):
    sizes = []
    s = bs.select(".option_cont > select")
    assert len(s) == 1
    ns = bs.select(".option_cont > select > option")
    for size in ns:
        size = size.text.replace(" ", "").replace("\n", "")
        if ('옵션선택' not in size and "(품절)" not in size):
            sizes.append(size)
    return sizes


@timeit
def extract_musinsa_product_detail_images(bs):
    pattern = regex.compile('(?<=<img alt=".+?" src=").+?(?=")')
    urls = pattern.findall(str(bs.select_one('#detail_view')))
    for url in urls:
        if (".gif" in url):
            #gif_index = urls.indexof(url)
            urls.remove(url)
    return urls


@timeit
def extract_musinsa_product_banner_images(bs):
    banners = bs.select(".product_thumb > li > img")
    banner_urls = []
    for banner in banners:
        banner = banner.get("src")
        if (".jpg" in banner):
            banner = f'https:{banner.replace("60.jpg", "500.jpg")}'
            banner_urls.append(banner)
    return banner_urls


@timeit
def extract_musinsa_product_tag_list(bs):
    atags = bs.select("li.article-tag-list > p.product_article_contents > a")
    gender = bs.select_one(".txt_gender > span").text
    brand = bs.select_one(
        ".product_article_contents > strong > a").text.replace(" ", "")
    category = bs.select_one(".item_categories").text.split(
        ">")[-1].split("\n")[0].replace(" ", "")
    tags = []
    for tag in atags:
        tags.append(tag.text[1:])
    tags.append(gender)
    tags.append(brand)
    tags.append(category)
    return tags


def parse_product(html):
    bs = BeautifulSoup(html, 'html.parser')
    product = {}
    product['title'] = extract_musinsa_product_title(bs)
    product['price'] = extract_musinsa_product_price(bs)
    product['video_link'] = None
    product['category'] = extract_musinsa_product_category(bs)
    product['description'] = None
    product['image'] = extract_musinsa_product_image(bs)
    product['brand'] = extract_musinsa_product_brand(bs)
    product['competitor_price'] = extract_musinsa_product_competitor_price(bs)
    product['shipping'] = 0
    product['size_array'] = extract_musinsa_product_size_array(bs)
    product['detail_images'] = extract_musinsa_product_detail_images(bs)
    product['banner_images'] = extract_musinsa_product_banner_images(bs)
    # product['item_link']=url
    product['influencer_show'] = True
    product['styled_image'] = extract_musinsa_product_image(bs)
    product['tag_list'] = extract_musinsa_product_tag_list(bs)
    product['item_type'] = "default"
    return product
