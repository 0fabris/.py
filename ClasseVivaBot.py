#!/usr/bin/python

# ClasseViva Message Checker
# 0fabris
# 03/2020 
# Visualizza i messaggi nella prima aula virtuale disponibile ogni 30 secondi. (forse per verificare presenza studente in aula) 
#

import re
import json
import requests
import os
import sys
import base64
import time
from urllib.parse import urlencode

#File dove sono salvate le credenziali
FNAME = "cv-auth.json"

#Bot
class CVBot():
    def __init__(self,usr,psw):
        self.tinit = time.time()
        self.CV_URL = "https://web.spaggiari.eu"
        self.headers = {
            "User-Agent" : "Mozilla/5.0",
            "Cookie": "",
            "Referer" : self.CV_URL,
            "Origin" : self.CV_URL,
            "Host":  self.CV_URL.split('//')[-1],
            "Pragma" : "no-cache",
            "Cache-Control" : "no-cache",
            "Accept":"*/*"
        }
        self.me_infos = self.Login(usr,psw)
        self.headers["Cookie"] += "PHPSESSID=" +re.findall(r"PHPSESSID\=(.*?);",self.me_infos.headers["Set-Cookie"])[-1]+"; "
        self.log("Login Effettuato")
    
    def Login(self,usr,psw):
        args = {
            "cid": "",
            "uid" : usr,
            "pwd" : psw,
            "pin" : "",
            "target" : "",
        }
        data = urlencode(args)
        hds = {
                "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8"
            }
        hds.update(self.headers)
        r = requests.post(
            self.CV_URL + "/auth-p7/app/default/AuthApi4.php?a=aLoginPwd",
            data=data,
            headers = hds
            )
        return r if (r.status_code != 404) else self.Login(usr,psw)
        
    def getAuleVirtuali(self):
        pag_aule = requests.get(
            self.CV_URL+ "/cvp/app/default/sva_aule.php",
            headers = self.headers
            )
        return re.findall(r"aula_id\=\"(.*?)\"\>Entra",pag_aule.text)
        
    def getAulaContext(self,aulaid):
        pag_forum = requests.get(
            self.CV_URL + "/cvp/app/default/sva_user.php?aula_id="+aulaid+"&a=forum",
            headers = self.headers
        )
        return re.findall(r"ctx\=(.*?)\&",pag_forum.text)[0]

    def getMessaggi(self,ctx):
        data = urlencode({
            "ctx": ctx,
            "mpp" : 50,
            "p" : 1
            })
        
        hds = dict({
            "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
            },**self.headers)
        
        page_mess = requests.post(
            self.CV_URL + "/sps/app/default/SocMsgApi.php?a=acGetMsgPag",
            headers = hds,
            data = data
        )
        
        return page_mess

    def log(self,msg):
        print("[{}] {}".format(str(time.time()-self.tinit)[:10], msg))

def getCredenziali():
    global FNAME
    if not os.path.isfile(FNAME):
        with open(FNAME,"w") as f:
            json.dump({
                "username" : str(input("Inserisci nome utente ClasseViva: ")),
                "password" : base64.b64encode(bytes(input("Inserisci password: ").encode('utf-8'))).decode("utf-8")
            },f)
    
    with open(FNAME,"r") as f:
        fl = json.load(f)
        fl["password"] = base64.b64decode(bytes(fl["password"].encode("utf-8"))).decode("utf-8") 
    
    return fl

if __name__ == "__main__":
    #pausa di 10 minuti prima di ricontrollare i messaggi
    nSecPause = 600
    
    try:
        if len(sys.argv)==3:
            bot = CVBot(sys.argv[1],sys.argv[2])
        else:
            loginfos = getCredenziali()
            bot = CVBot(loginfos["username"],loginfos["password"])
        aula = bot.getAuleVirtuali()[0]
        ctx = bot.getAulaContext(aula)
    except:
        print("Errore nella procedura di entrata nell'aula virtuale")
        exit()

    mlist = None
    
    while True:
        try:
            res = bot.getMessaggi(ctx).json()
            
            if mlist is None or len(mlist["OAS"]["rows"]) != len(res["OAS"]["rows"]):
                mlist = res
                for msg in mlist["OAS"]["rows"]:
                    bot.log("Mittente: " + msg["sender"] + " ha detto " + msg["testo"] +" " + msg["date"])
                bot.log(f"ReCheck ogni {nSecPause} secondi.")
            else:
                bot.log("No nuovi messaggi")
        except:
            bot.log("Errore nella lettura dei messaggi")
        
        time.sleep(nSecPause)
    
