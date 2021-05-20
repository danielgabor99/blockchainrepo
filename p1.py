
import json
import datetime #for reading present date
import time 
import requests #for retreiving coronavirus data from web
from plyer import notification #for getting notification on your PC
import http.client
from threading import Thread
import csv
import sys

def showMessage(coinName, coinPrice, coinPercentage, oldPrice):
    notification.notify(
        title = "Coins Alert {}".format(datetime.datetime.now()),
        message = "{coinName}: {coinPrice}\nOld Price: {oldPrice} \nGrowing: {coinPercentage}%".format(
                    coinName=coinName,
                    coinPrice = coinPrice,
                    coinPercentage=coinPercentage,
                    oldPrice=oldPrice),
        timeout  = 5
    )



def process_id(id):
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
        
    return 0

def process_range(id_range, store=None):
    """process a number of ids, storing the results in a dict"""
    if store is None:
        store = {}
    for id in id_range:
        store[id] = process_id(id)
    return store

def threaded_process_range(nthreads, id_range):
    """process the id range in a specified number of threads"""
    store = {}
    threads = []
    # create the threads
    for i in range(nthreads):
        ids = id_range[i::nthreads]
        t = Thread(target=process_range, args=(ids,store))
        threads.append(t)

    # start the threads
    [ t.start() for t in threads ]
    # wait for the threads to finish
    [ t.join() for t in threads ]
    return store
def saveToCsv(OldValuesOfCoins):
    w = csv.writer(open("output.csv", "w"))
    for key, val in OldValuesOfCoins.items():
        w.writerow([key, val]) 

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

def readCoins():
    with open("symbols.txt") as f:
        listOfCoins = f.readlines()
    listOfCoins = [x.strip() for x in listOfCoins]
    return listOfCoins

def getOldValuesFromFile():
    mycsv = csv.reader(fix_nulls(open("output.csv")))
    mydict={}
    for row in mycsv:
        if(row!=[]):
            mydict[row[0]]=row[1]
    if(mydict=={}):
        print("csv empty, creating new one...")
        return threaded_process_range(100,readCoins())
    else:
        return mydict


def main(percentage):
    listOfCoins=readCoins()

    OldValuesOfCoins=getOldValuesFromFile()
    
    while(True):
        try:
            print("\ncalculating with {}% of growing...".format(percentage))
            NewValuesOfCoins=threaded_process_range(100,listOfCoins)
            for i in NewValuesOfCoins:
                if(NewValuesOfCoins[i]!=0 and OldValuesOfCoins[i]!=0 and NewValuesOfCoins[i]!='0' and OldValuesOfCoins[i]!='0'):
                    result= float(NewValuesOfCoins[i])*100/float(OldValuesOfCoins[i])-100
                    if(int(result)>percentage):
                        print(i.upper()+":", "new price: "+NewValuesOfCoins[i], "old: "+OldValuesOfCoins[i], str(int(result))+"%")
                        showMessage(i.upper(), NewValuesOfCoins[i], int(result), OldValuesOfCoins[i])
            OldValuesOfCoins=NewValuesOfCoins
            saveToCsv(OldValuesOfCoins)
        
        except:
            OldValuesOfCoins=NewValuesOfCoins
            saveToCsv(OldValuesOfCoins)
            print("\nrecalculating...")          
        
         
if __name__ == "__main__":
    percentage = int(sys.argv[1])
    main(percentage) 
    