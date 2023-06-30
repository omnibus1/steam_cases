import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import json
import sys
import sqlite3
import time
from random import randint

con=sqlite3.connect("steam_data.sqlite")
cur=con.cursor()

if len(sys.argv)==2 and sys.argv[1]=="--setup":
    cur.execute("drop table if exists cases")
    cur.execute("create table cases (name text, date text, price real, quantity integer)")
    exit()

arr=json.load(open("urls.json","r"))

for val in arr:
    url=val["url"]
    #get last part of url and get the name of the case from it
    name=url.split("/")[-1].replace("%20"," ")
    #both times the same, usually fixes by itselve
    attempts=0
    while attempts<4:
        try:
            time.sleep(randint(5,15))
            page=requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            scipt_tag=soup.find_all("script",type="text/javascript")
            price_history=scipt_tag[27].get_text()
            break

        except:
            attempts+=1
            print(f"tried again {attempts}")

    data=re.search("\[\[.*\]\]",price_history).group(0)
    data=data[1:-1]

    print(name)
    last_24=data.split(",")[-24*3:]
    for i in range(0,len(last_24),3):
        date=last_24[i][2:-5]+":00"
        price=last_24[i+1]
        quantity=last_24[i+2][1:-2]
        cur.execute(f"insert into cases values('{name}','{date}','{price}','{quantity}')")
        con.commit()
    open("hello.txt","w")
    time.sleep(3)


