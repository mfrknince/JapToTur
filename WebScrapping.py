from bs4 import BeautifulSoup
import requests
from PIL import Image
from io import BytesIO

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}

def find_anime_picture(name):
    url = "https://www.fandom.com/?s=" + name

    response = requests.get(url,headers= header)
    soup = BeautifulSoup(response.content, "html.parser")
    rows = soup.find("div",{"class":"grid-block wrap posts post-list"})
    row=rows.find("div",{"data-absolute-position":"1"})
    img_tag = row.find("img")
    if img_tag and "src" in img_tag.attrs:
        return  img_tag["src"]

def load_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return image



