import requests
import io
from PIL import Image
import numpy as np
from rembg.bg import remove
import time
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
def remove_background(image_url):
    start = time.time()
    response = requests.get(image_url, stream=True, headers=headers)
    point1 = time.time() - start
    image = Image.open(io.BytesIO(response.content))
    point2 = time.time() - point1
    result = remove(response.content)
    point3 = time.time() - point2
    image = Image.open(io.BytesIO(result)).convert('RGBA')
    point4 = time.time() - point3
    print(point1, point2, point3, point4)
    return image