import http.client

conn = http.client.HTTPSConnection('api.cryptonator.com')

conn.request("GET", "/api/ticker/btc-usd")
r1 = conn.getresponse()
data=r1.read()

a=data.decode()




priceString='"price":"'
coinPrice=a.split(priceString, 1)[1].split('"', 1)[0]

nameString='"success":'
coinName=a.split(nameString, 1)[1].split(',', 1)[0]


def getPercent(old,new):
    return new*100/old-100



import csv



def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

mycsv = csv.reader(fix_nulls(open("output.csv")))
mydict={}
for row in mycsv:
    if(row!=[]):
        mydict[row[0]]=row[1]
for i in mydict:
    print(i.upper()+" dsa")





try:
    requests.get("http://127.0.0.1:8000/test/",timeout=0.0000000001)
except requests.exceptions.ReadTimeout: 
    pass


--hidden-import plyer.platforms.win.notification

