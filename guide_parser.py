#!/usr/bin/python
'''

    Programma leggi guida per la data odierna
    Rai & Mediaset
    Python3
    Coded by 0fabris

'''
import requests,re,datetime,time,json

class GuidaTV():
    def __init__(self):
        self.oggi = '-'.join(n for n in str(datetime.datetime.now().date()).split('-')[::-1])
        self.nomefile = 'guida.txt'
        with open(self.nomefile,'w') as fl:
            fl.write(' --- Aggiornamento per data odierna ' + self.oggi + ' ---\n')
        
        self._guidaRAI()
        self._guidaMediaset()

    def _guidaRAI(self):
        url = 'https://www.raiplay.it/guidatv/?giorno={}'.format(self.oggi)
        page = requests.get(url).text
        programmi = []
        for i in re.findall(r"<ol data-channel=\".*?\" class=\"program\">",page): #separa canali
            tmp = page.split(i)[1].split('</ol>')[0].split('</div></li>')
            for x in tmp: #per ogni canale ##separa programmi tv
                name = str(re.findall(r"<p class=\"nameChannel\">(.*?)</p>",x)).replace('[','').replace(']','').replace('\'','')
                info = str(re.findall(r"<p class=\"info\">(.*?)</p>",x)).replace('[','').replace(']','').replace('\'','')
                epis = str(re.findall(r"<p class=\"subtitle\">(.*?)</p>",x)).replace('[','').replace(']','').replace('\'','')
                desc = str(re.findall(r"<p class=\"descProgram\">(.*?)</p>",x)).replace('[','').replace(']','').replace('\'','')
                ora = self.oggi + ' ' + str(re.findall(r"<p class=\"time\">(.*?)</p>",x)).replace('[','').replace(']','').replace('\'','')+':00'
                if(name):
                    programmi.append(Programma(name,info,epis,desc,ora))
        self.writeOnGuide(programmi)

    def _guidaMediaset(self):
        url = 'https://api-ott-prod-fe.mediaset.net/PROD/play/alive/allListingFeedEpg/v1.0?byListingTime={}~{}&byCallSign={}' #https://api-ott-prod-fe.mediaset.net/PROD/play/alive/allListingFeedEpg/v1.0?byListingTime=1564520400000~1564628400000&byCallSign=C5
        chans = ['C5','I1','R4','LB','KA','I2','KQ','FU','LT','KI','KB','LA','KF','W1']
        timenow = int(time.mktime(datetime.datetime.now().date().timetuple())-3600)*1000
        programmi = []
        for i in chans:
            nurl = url.format((timenow),timenow+108000000,i)
            page = json.loads(requests.get(nurl).text)['response']['entries'][0]
            name = re.findall(r"'title': '(.*?)'",str(page['stations']))[0]
            for x in page['listings']:
                info = x['mediasetlisting$epgTitle']
                epis = ''
                desc = x['description']+ ' ' + x['mediasetlisting$shortDescription']
                ora = datetime.datetime.fromtimestamp(x['startTime']/1000)
                programmi.append(Programma(name,info,epis,desc,ora))
        self.writeOnGuide(programmi)

    def writeOnGuide(self,programmi):
        with open(self.nomefile,'a+') as fl:
                for i in programmi:
                    fl.write(i.returnProgramma())

class Programma():
    def __init__(self,nome,info,epis,desc,ora):
        self.nome = nome
        self.info = info
        self.epis = epis
        self.desc = desc
        self.ora = ora

    def printProgramma(self):
        print(self.returnProgramma())    

    def returnProgramma(self):
        return '\nNome canale: {}\nInfo: {}\nEpisodio: {}\nDescrizione: {}\nOra: {}\n'.format(self.nome,self.info,self.epis,self.desc,self.ora)

if __name__ == '__main__':
    GuidaTV()
    print('terminato')