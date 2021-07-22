from product_crawler import crawl_musinsa_product_html2
from parser import parse_product_html

html = crawl_musinsa_product_html2('1005314')
print(parse_product_html('1005314', html))
#1005314: 사이즈 테이블 없고, 옵션 블랙 자동 설정 + 사이즈 옵션 따로
#1876370: 사이즈테이블 있고, 옵션 화이트 자동 설정됨