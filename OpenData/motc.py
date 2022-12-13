import requests
from bs4 import BeautifulSoup

r1 = requests.get("https://www.motc.gov.tw/ch/index.jsp")
b1 = BeautifulSoup(r1.text, "html.parser")
ret = b1.find('div', {'id':"accesskey"}).find_all('span', {"class": "left"})
for d in ret:
    print(d.text)
    