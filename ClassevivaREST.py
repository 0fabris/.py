
#'''''''''''''''''''#
#                   #
# ClasseViva2Python #
#(REST API  Version)#
#   coded by me   #
#                   #
#'''''''''''''''''''#

import urllib, urllib2, json, base64, time

baseurl = 'https://web.spaggiari.eu/rest/v1'

try:
    loginfile = file('classeviva_python-login.json','r')
    file1 = json.loads(loginfile.read())
    print 'Bentornato, il programma e\' in caricamento...\n'
    user = file1['username']
    print '\nTi stai loggando con l\' account %s\n' % user
    passw = base64.b64decode(file1['password'])
    loginfile.close()
    
except:
    print 'Benvenuto/a, mi sembra che non hai ancora inserito i tuoi dati...\n'
    user = raw_input('Inserisci l\' Utente:\n---->')
    passw = raw_input('Inserisci la Password:\n---->')
    loginfile = file('classeviva_python-login.json','w')
    jsonfile = {
        'username':user,
        'password':base64.b64encode(passw),
        }
    json.dump(jsonfile, loginfile)
    loginfile.close()
    
class ClasseVivaRest():
    
    def Login(self,user,passw):
        import urllib2, urllib,json
        args = "{\"pass\":\""+passw+"\",\"uid\":\""+user+"\"}"
        rpage = urllib2.Request(baseurl+'/auth/login',args)
        rpage.add_header('Content-Type','application/json')
        rpage.add_header('Z-Dev-Apikey','+zorro+')
        rpage.add_header('User-Agent','zorro/1.0')
        page = urllib2.urlopen(rpage).read()
        return json.loads(page)

    def getApiResp(self,apiurl,token):
        import urllib2, json
        rpage = urllib2.Request(apiurl)
        rpage.add_header('Content-Type','application/json')
        rpage.add_header('Z-Dev-Apikey','+zorro+')
        rpage.add_header('Z-Auth-Token',token)
        rpage.add_header('User-Agent','zorro/1.0')
        page = urllib2.urlopen(rpage).read()
        return json.loads(page)

    def getAssenze(self,ident,token):
        pass

    def getAgenda(self,ident,token):
        pass

    def getToday(self,ident,token):
        listamat = []
        apiresp = self.getApiResp(baseurl+'/students/%s/%s' %(ident[1:-1],'lessons/today'),token)['lessons']
        if apiresp == []:
            print '\n - Oggi non hai avuto lezioni - \n'
            return None
        for i in apiresp:
            listamat.append(i['lessonType']+'@'+i['authorName']+'@'+str(i['evtHPos'])+'@'+i['lessonArg']+'@'+i['subjectDesc']+'@'+str(i['evtDuration']))
        print '\n\n'
        for i in listamat:
            lista1 = i.split('@')
            ltyp, prof, n_ora, arg, desc, durata = lista1
            print '%s ora di durata %sh (%s di %s) - Prof. %s => %s\n' %(n_ora,durata,ltyp,desc,prof,arg)

    def getGrades(self,ident,token):
        listavoti = []
        for i in self.getApiResp(baseurl+'/students/%s/%s' %(ident[1:-1],'grades'),token)['grades']:
            listavoti.append(i['subjectDesc']+'@'+i['displayValue']+'@'+i['componentDesc']+'@'+i['evtDate'])
        print '--- Voti ---\n'
        for i in listavoti:
            lista1 = i.split('@')
            materia = lista1[0]
            voto = lista1[1]
            tipo = lista1[2]
            datains = lista1[3]
            print '%s - %s - Tipo: %s - Data: %s\n\n' %(materia,voto,tipo,datains)
        #print '--- ---- ---\n'
            
    def getLessons(self,ident,token):
        print self.getApiResp(baseurl+'/students/%s/%s' %(ident[1:-1],'subjects'),token)

    def getNotes(self,ident,token):
        pass

    def getCircolari(self,ident,token):
        a = self.getApiResp(baseurl+'/students/%s/%s' %(ident[1:-1],'noticeboard'),token)
        listacirc = []
        for i in a['items']:
            listacirc.append(str(i['readStatus'])+'@'+i['cntTitle']+'@'+str(i['evtCode'])+'@'+str(i['pubId'])+'@'+i['cntCategory'])
        cont = 1
        for b in listacirc:
            circ = b.split('@')
            if circ[0] == 'True':
                stat = 'Letta'
            else:
                stat = 'Non letta'
            print str(cont)+' - '+circ[1]+' - '+stat+' - '+circ[-1]
            cont += 1
        voglia = input('\nVuoi Scaricare una Circolare?\n    1:Si\n    2:No\n\n---->')
        while voglia == 1:
            numcirc = cont +1
            while numcirc>cont:
                numcirc = input('\nScrivi il numero della Circolare\n\n---->')
                if numcirc > cont:
                    print 'Reinserisci in numero della circolare\n\n'
            circ_1 = listacirc[numcirc-1].split('@')
            circtype = circ_1[-1]
            if circtype == 'News':
                print '\nQuesto tipo di Circolare non si puo\' scaricare!\n'
                break
            if circtype == 'Circolare' or circtype == 'Scuola/famiglia':
                c = urllib2.Request(baseurl+'/students/%s/%s' %(ident[1:-1],'noticeboard/attach/'+circ_1[2]+'/'+circ_1[3]+'/101'))
                c.add_header('User-Agent','zorro/1.0')
                c.add_header('Z-Dev-Apikey','+zorro+')
                c.add_header('Z-Auth-Token',token)
                pagepdf = urllib2.urlopen(c)
                filepdf = file('circolare_'+ident+'_'+str(numcirc)+'.pdf','wb')
                filepdf.write(pagepdf.read())
                filepdf.close()
                print 'File Scritto'
            voglia = input('\nVuoi scaricare un\' altra circolare?\n\n    1:Si\n    2:No\n\n---->')
            
    def getSubjects(self,ident,token):
        pass

    def StudentInfo(self,ident,token):
        infos = self.getApiResp(baseurl+'/students/%s/%s' %(ident[1:-1],'card'),token)['card']
        print 'Codice Id Spaggiari: %s\n\nNome: %s\n\nCognome: %s\n\nNome Scuola: %s %s\n\nCodice Miur: %s - Codice Spaggiari: %s\n\nCodice Fiscale: %s' %(infos['ident'],infos['firstName'],infos['lastName'],infos['schName'],infos['schDedication'],infos['miurSchoolCode'],infos['schCode'],infos['fiscalCode']) 
        
    def Registro(self,user,passw,token,home,exp):
        while True:
            print "1 - Visualizza i voti\n\n2 - Visualizza cosa hai fatto oggi\n\n3 - Visualizza le lezioni\n\n4 - Visualizza le circolari\n\n5 - Guarda le informazioni sullo studente\n\n6 - LogOut e Uscire\n"
            azione = input('\nScegli il numero dell\' azione da fare:\n\n---->')
            if exp <= time.time():
                    print '\nRichiedo un nuovo Token per Accedere al registro\n'
                    home = self.Login(user,passw)
                    token = home['token']
            if azione == 1:
                self.getGrades(home['ident'],token)
            elif azione == 2:
                self.getToday(home['ident'],token)
            elif azione == 3:
                self.getLessons(home['ident'],token)
            elif azione == 4:
                self.getCircolari(home['ident'],token)
            elif azione == 5:
                self.StudentInfo(home['ident'],token)
            elif azione == 6:
                print 'Arrivederci'
                break
            else:
                print '\nNon hai scelto nessuna azione, Arrivederci!'
                break

            voglia = input('\nVuoi ancora usare il programma? (1:Si,0:No)\n\n---->')
            if voglia == 0:
                print '\nArrivederci!\n'
                break
            elif voglia == 1:
                if exp <= time.time():
                    print '\nRichiedo un nuovo Token per Accedere al registro\n'
                    home = self.Login(user,passw)
                    token = home['token']
                print '\nOK, scegli di nuovo un\' azione:\n'
            else:
                print '\nNon hai scelto ne\' si ne\' no...\nQuindi, Arrivederci!\n'
                break
            
    def __init__(self):
        l = self.Login(user,passw)
        finetoken = time.time()+3600
        print 'Connesso...\n\nBenvenuto/a %s, Num. %s\n' % (l['firstName'], l['ident'][1:-1])
        self.Registro(user,passw,l['token'],l,finetoken)

if __name__ == '__main__':
    ClasseVivaRest()
