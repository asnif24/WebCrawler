import requests
import json
 
res = requests.get(
    url='https://soa.tainan.gov.tw/Api/Service/Get/00693eb9-4ddc-4c40-a668-cb7210f7c742',
    verify=False    
)
res = json.loads(res.text)

for d in res['data']:
    print(d)