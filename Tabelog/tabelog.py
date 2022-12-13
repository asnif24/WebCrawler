from cgitb import html
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from pyparsing import col

df = pd.DataFrame(columns=["Rating", "JA", "EN", "url"])
page = 59
while True:
    url = f"https://tabelog.com/tw/tokyo/rstLst/{page}/?SrtT=rt"
    print("process url:", url)
    try:
        response = urlopen(url)
    except HTTPError:
        print("End!")
        break
    html = BeautifulSoup(response, features="html.parser")

    # find: 找第一個符合條件 -> 一個答案 ; find_all: 找所有符合條件 -> 一個List
    # print(html.find_all('li', {"class":"list-rst"}))
    for r in html.find_all('li', class_="list-rst"):
        ja = r.find("small", class_="list-rst__name-ja")
        en = r.find("a", class_="list-rst__name-main")
        rating = r.find("b", class_="c-rating__val")
        # 萃取紙條(.text) ; 萃取特徵([特徵])
        print(rating.text, ja.text, en.text, en["href"])
        s = pd.Series([rating.text, ja.text, en.text, en["href"]],
                      index=["Rating", "JA", "EN", "url"])
        df = df.append(s, ignore_index=True)
        # use pd.concat !?
    page += 1

df.to_csv("tabelog.csv", encoding="utf-8", index=False)

# print(df)
