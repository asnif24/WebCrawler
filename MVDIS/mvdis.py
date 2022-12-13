
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
import json
import datetime


with open('mvdis.json', encoding="utf-8") as f:
    mvdis_data = json.load(f)


mvdis_url = "https://www.mvdis.gov.tw/m3-emv-plate/webpickno/queryPickNo"
captcha_url = "https://www.mvdis.gov.tw/m3-emv-plate/captchaImg.jpg"

h = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
     "Accept-Encoding": "gzip, deflate, br",
     "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-CN;q=0.5",
     "Cache-Control": "max-age=0",
     "Connection": "keep-alive",
     "Cookie": 'DWRSESSIONID=tNG0MdxettRHrCcz6yf*mYGBaao; _ga=GA1.3.1538469191.1659018978; _gid=GA1.3.204515142.1660153474; BSESSIONID1=CA803AF53E4DD6F31CF240E86960B19C.tsb12; JSESSIONID1=9BC6A27AC244DB24135BB0F45778CB69.tsp11; ADRUM_BTa="R:59|g:9af7fc30-d8db-400b-9a3c-159197f77717|n:customer1_b3bb7d45-77a0-4845-9079-72c1a6bc63f9"; SameSite=None; ADRUM_BT1="R:59|i:28292|e:381"; _gat=1; _gat_gtag_UA_81912319_9=1',
     "Host": "www.mvdis.gov.tw",
     "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
     "sec-ch-ua-mobile": "?0",
     "sec-ch-ua-platform": '"Windows"',
     "Sec-Fetch-Dest": "document",
     "Sec-Fetch-Mode": "navigate",
     "Sec-Fetch-Site": "none",
     "Sec-Fetch-User": "?1",
     "Upgrade-Insecure-Requests": "1",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
     }


r = requests.get(
    mvdis_url,
    headers=h)

b = BeautifulSoup(r.text, features="html.parser")
b_csrf = b.find('input', {"name": "CSRFToken"})
csrf = b_csrf["value"]
print(csrf)


# payload constant
method = "qryPickNo"
selWindowNo = "01"
selCarType = "C"
selEnergyType = "E"
selPlateType = "g"
plateVer = "2"
queryType = "0"
queryNo = "*"


df = pd.DataFrame(columns=["plate", "selDeptName",
                  "selStationName", "location"])
for i in range(len(mvdis_data)):
    craw = True
    while craw:
        craw = False
        r_captcha = requests.get(
            captcha_url,
            headers=h)
        img_name = "./captcha/" + \
            ("000000"+str(len(os.listdir("./captcha"))))[-6:]
        with open(img_name+".jpg", 'wb') as f:
            f.write(r_captcha.content)

        cap = input(f"cap{i}: ").upper()
        os.rename(img_name+".jpg", img_name+"_"+cap+".jpg")
        payload = {
            "method": "qryPickNo",
            "selDeptCode": mvdis_data[i]["selDeptCode"],
            "selStationCode": mvdis_data[i]["selStationCode"],
            "selWindowNo": "01",
            "location": mvdis_data[i]["location"],
            "selCarType": "C",
            "selEnergyType": "E",
            "selPlateType": "g",
            "plateVer": "2",
            "validateStr": cap,
            "queryType": "0",
            "queryNo": "*",
            "CSRFToken": csrf
        }
        r_p = requests.post(
            mvdis_url,
            headers=h,
            data=payload
        )
        b_p = BeautifulSoup(r_p.text, features="html.parser")

        if b_p.find('td', {"id": "headerMessage"}).text == "驗證數字輸入錯誤":
            craw = True
            continue

        nums = b_p.find_all('a', {"class": "number"})
        for num in nums:
            df_tmp = pd.DataFrame([[
                num.text, mvdis_data[i]["selDeptName"],
                mvdis_data[i]["selStationName"],
                mvdis_data[i]["location"]]],
                columns=["plate", "selDeptName", "selStationName", "location"])
            df = pd.concat([df, df_tmp], ignore_index=True)

        try:
            total_count = int(
                (b_p.find("div", {"class": "align_c note"})).text.split()[1])
        except:
            continue

        if total_count > 65:
            page_params = {
                "d-3611679-p": 2,
                "method": "queryPickNoView"
            }
            r_page2 = requests.get(
                mvdis_url,
                headers=h,
                params=page_params
            )
            b_page2 = BeautifulSoup(r_page2.text, features="html.parser")
            nums_page2 = b_page2.find_all('a', {"class": "number"})
            for num in nums_page2:
                df_tmp = pd.DataFrame([[
                    num.text, mvdis_data[i]["selDeptName"],
                    mvdis_data[i]["selStationName"],
                    mvdis_data[i]["location"]]],
                    columns=["plate", "selDeptName", "selStationName", "location"])
                df = pd.concat([df, df_tmp], ignore_index=True)

df.to_csv(f"./plates/mvdis_{datetime.date.today()}.csv", encoding="utf-8", index=False)
df_sorted = df.sort_values(by="plate")
df_sorted.to_csv(f"./plates/mvdis_{datetime.date.today()}_sorted.csv", encoding="utf-8", index=False)
# df.to_csv("mvdis.csv", encoding="utf-8", index=False)
