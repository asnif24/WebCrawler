from urllib.request import urlopen, urlretrieve
import json
import os

# # for Mac only
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

for m in range(12):
    url = "https://www.google.com/doodles/json/2021/10?hl=zh-TW"
    response = urlopen(url)
    doodles = json.load(response)

    # doodles -> List; d -> dictionary
    for d in doodles:
        # print(d["title"], d["alternate_url"])
        url = "https:"+d["url"]
        print(d["title"], url)
        dirname = "./doodles/{}/".format(m+1)
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        fname = dirname+url.split('/')[-1]
        
        # # 太常用 有包起來!
        # # 針對圖片做處理
        # response = urlopen(url)
        # img = response.read()
        # # 存檔三部曲
        # f = open(fname, "wb")
        # f.write(img)
        # f.close()
        urlretrieve(url, fname)






