import csv
import requests
import json
# import io
r1 = requests.get("	https://sports.tms.gov.tw/opendata/sports_tms.json"
                  )
print(r1.encoding)
print(r1.text)

# f = io.StringIO(r1.text)
# ret = list(csv.reader(f))
jj = json.loads(r1.text)
for d in jj:
    print(d["Area"], d["Name"], d["Address"])
