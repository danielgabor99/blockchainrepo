
import json
import datetime #for reading present date
import time 
import requests #for retreiving coronavirus data from web
from plyer import notification #for getting notification on your PC
import http.client
from threading import Thread
import csv
import sys
mylist=[]


def fetchCoinValue(id):
    
    conn = http.client.HTTPSConnection('api.binance.com')
    conn.request("GET", "/api/v1/ticker/price?symbol={}USDT".format(id.upper()))
    r1 = conn.getresponse()

    data=r1.read()
    dataInString=data.decode()
    
    priceString='"price":"'

    if(dataInString.find('code')!=-1):
       
        conn.request("GET", "/api/v1/ticker/price?symbol={}BUSD".format(id.upper()))
        r1 = conn.getresponse()

        data=r1.read()
        dataInString=data.decode()

        priceString='"price":"'
        if(dataInString.find('code')==-1):
            currentCoinPrice=dataInString.split(priceString, 1)[1].split('"', 1)[0]
            return currentCoinPrice
        else:
            try:
                conn = http.client.HTTPSConnection('api.cryptonator.com')
                conn.request("GET", "/api/ticker/{}-usd".format(id))
                r1 = conn.getresponse()
            
                data=r1.read()
                dataInString=data.decode()

                successString='"success":'
                Success=dataInString.split(successString, 1)[1].split(',', 1)[0]

                if(Success=="true"):
                    priceString='"price":"'
                    currentCoinPrice=dataInString.split(priceString, 1)[1].split('"', 1)[0]
                    return currentCoinPrice
            except:
                print(0)
        
    else:
        currentCoinPrice=dataInString.split(priceString, 1)[1].split('"', 1)[0]
        return currentCoinPrice  



    # except:
    #     print("something with the request happend..")
    #     global ok
    #     ok=0
    #     return -1
        
    # return 0

def readCoins():
    with open("symbolsbinance.txt") as f:
        listOfCoins = f.readlines()
    listOfCoins = [x.strip() for x in listOfCoins]
    return listOfCoins

def fetchAllCoins(listOfCoins):
    store={}
    i=1

    for id in listOfCoins:
        
        i=i+1
        k=fetchCoinValue(id)
    
    print(len(mylist))
        


print(fetchCoinValue('one'))
