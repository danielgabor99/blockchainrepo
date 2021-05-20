
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

def showStartMessage():
    notification.notify(
        title = "program started",
        message = "started",
        timeout  = 5
    )

def showVPNMessage():
    notification.notify(
        title = "VPN ERROR",
        message = "ERROR",
        timeout  = 5
    )


def fetchCoinValue(id):
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
        print("something with the request happend..")
        global ok
        ok=0
        return -1
        
    return 0

def fetchAllCoins(listOfCoins):
    store={}
    i=1
    for id in listOfCoins:
        print(i, id)
        i=i+1
        store[id] = fetchCoinValue(id)
        if(store[id]==-1):
            showVPNMessage()
            break
    return store

def saveToCsv(OldValuesOfCoins):
    w = csv.writer(open("longoutputbinance.csv", "w"))
    for key, val in OldValuesOfCoins.items():
        w.writerow([key, val])

def saveToTxt(Coin):
    with open("longgrowings.txt", "a") as text_file:
        text_file.write("\n"+Coin) 

def checkIfMultipleIncreases(id):
    data = open('longgrowings.txt').read()
    count = data.count(id.upper())
    return count

def print_time():   
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = "\n\nValues calculated at: " + current_time
    return data

def SaveVpnErrorTxt():
    with open("longgrowings.txt", "a") as text_file:
            text_file.write("\nVPN ERROR FOR THIS CALCULATION :(")
def SaveNoChangesMadeTxt():
    with open("longgrowings.txt", "a") as text_file:
            text_file.write("\nNo changes were made in this calculation")

def fix_nulls(s):
    for line in s:
        yield line.replace('\0', ' ')

def readCoins():
    with open("symbolsbinance.txt") as f:
        listOfCoins = f.readlines()
    listOfCoins = [x.strip() for x in listOfCoins]
    return listOfCoins

def getOldValuesFromFile(listOfCoins):
    mycsv = csv.reader(fix_nulls(open("longoutputbinance.csv")))
    mydict={}
    for row in mycsv:
        if(row!=[]):
            mydict[row[0]]=row[1]
    if(mydict=={}):
        print("csv empty, creating new one...")
        return fetchAllCoins(listOfCoins)
    else:
        return mydict


def main(percentage):
    global ok
    ok=1
    changesMade=0
    listOfCoins=readCoins()

    OldValuesOfCoins=getOldValuesFromFile(listOfCoins)
    
    
    try:
        with open("longgrowings.txt", "a") as text_file:
            text_file.write(str(print_time()))

        print("\ncalculating with {}% of growing...".format(percentage))
        NewValuesOfCoins=fetchAllCoins(listOfCoins)
        

        if(len(NewValuesOfCoins)>100):
            if(ok==1):
                showStartMessage()

            for i in NewValuesOfCoins:
                if(NewValuesOfCoins[i]!=0 and OldValuesOfCoins[i]!=0 and NewValuesOfCoins[i]!='0' and OldValuesOfCoins[i]!='0'):
                    result= float(NewValuesOfCoins[i])*100/float(OldValuesOfCoins[i])-100
                    if(int(result)>percentage):
                        print(i.upper()+":", "new price: "+NewValuesOfCoins[i], "old: "+OldValuesOfCoins[i], str(int(result))+"%")
                        if(checkIfMultipleIncreases(i)>1):
                            print(i," appeared {} times already".format(checkIfMultipleIncreases(i)+1))
                            saveToTxt(i.upper()+"({})".format(checkIfMultipleIncreases(i)+1)+": "+ "new price: "+NewValuesOfCoins[i]+ " old: "+OldValuesOfCoins[i]+" "+ str(int(result))+"%")
                        else:
                            saveToTxt(i.upper()+": "+ "new price: "+NewValuesOfCoins[i]+ " old: "+OldValuesOfCoins[i]+" "+ str(int(result))+"%")
                        changesMade=1
                        #showMessage(i.upper(), NewValuesOfCoins[i], int(result), OldValuesOfCoins[i])
            OldValuesOfCoins=NewValuesOfCoins
            saveToCsv(OldValuesOfCoins)
            if(changesMade==0):
                SaveNoChangesMadeTxt()


        else:
            SaveVpnErrorTxt()
    
    except:
        OldValuesOfCoins=NewValuesOfCoins
        saveToCsv(OldValuesOfCoins)
        print("\nrecalculating...")          
        
         
if __name__ == "__main__":
    percentage = 25
    main(percentage) 
    