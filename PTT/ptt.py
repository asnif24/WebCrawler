from cgitb import html
from urllib import response
from bs4 import BeautifulSoup
import requests

url = "https://www.ptt.cc/bbs/PC_Shopping/M.1659945964.A.C02.html"
response = requests.get(url)
html = BeautifulSoup(response.text, features="html.parser")

content = html.find('div', id="main-content")
metas = content.find_all("span", class_="article-meta-value")
print(metas)