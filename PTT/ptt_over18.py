from cgitb import html
from urllib import response
from bs4 import BeautifulSoup
import requests

url = "https://www.ptt.cc/bbs/Gossiping/M.1660127941.A.A04.html"
response = requests.get(url, cookies={"over18": "1"})
html = BeautifulSoup(response.text, features="html.parser")
# html = BeautifulSoup(response.text)


content = html.find('div', id="main-content")
metas = content.find_all("span", class_="article-meta-value")
print(metas[0].text)
print(metas[1].text)
print(metas[2].text)
print(metas[3].text)
