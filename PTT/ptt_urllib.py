from urllib import response
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

url = "https://www.ptt.cc/bbs/PC_Shopping/M.1659945964.A.C02.html"
r = Request(url)
r.add_header("user-agent", "Mozilla/5.0")
response = urlopen(r)
html = BeautifulSoup(response)
print(html)