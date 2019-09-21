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
        #with open(self.nomefile,'w') as fl:
        #    fl.write(' --- Aggiornamento per data odierna ' + self.oggi + ' ---\n')
        
        self._guidaRAI()
        self._guidaMediaset()
        self._guidaRSI()

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

    def _guidaRSI(self):
        '''
        url = 'https://www.rsi.ch/palinsesto/'
        wcontid = re.findall(r"data-widget-new-slider-schedule-id=\"(.*?)\"",requests.get(url).text)[0]
        #.split('</div><!-- /.time -->')[1].split('</div><!-- /.vectors -->')[0].replace('\n','').split('<!-- /.prog-content -->')[:-1]
        url_epg = 'https://www.rsi.ch/?'
        dataoggi = datetime.datetime.now()
        args = {
            'widgetContentId': wcontid,
            'widgetName': 'epg',
            'widgetView': 'newSliderSchedule',
            'ajax':'true',
            'ajaxType':'tv',
            'customDate': str(dataoggi).split(' ')[0]
        }
        headers = {
            'Referer' : 'https://www.rsi.ch/palinsesto/',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
            'Cookie': 'POPUPCHECK=1569158606987; JSESSIONID=9A9F2AC4846769241D4F38473B1E2B5F; wt_rla=292330999892453%2C6%2C1569074224871; wt_geid=815590587640031778717787; _sg_b_v=3%3B3447%3B1569075665; sliderDayID=new_slide_schedule_day-sab-2019-09-21; wt_cdbeid=1; wt_r=1; _sg_b_p=%2Fpalinsesto%2F',
            'X-Requested-With': 'XMLHttpRequest',
            'Host' : 'www.rsi.ch',
            'Pragma' : 'no-cache',
            'Accept' : '*/*',
            'DNT' : '1',
        }
        urlepg_today = url_epg + urllib.parse.urlencode(args)
        print(urlepg_today)
        page = requests.post(urlepg_today,data=args,headers=headers).text
        print(page)
        return
        programmi = []
        for i in page:
            name = 'RSI '+re.findall(r"data-prog-vector=\"(.*?)\">",i)[0]
            info = re.findall(r"data-prog-title = \"(.*?)\"",i)[0]
            desc = re.findall(r"data-prog-description = \"(.*?)\"",i)[0]
            epis = ''
            ora = re.findall(r"data-prog-currentDay=\"(.*?)\"",i)[0] + ' ' + re.findall(r"data-prog-startTime = \"(.*?)\"",i)[0]
            programmi.append(Programma(name,info,epis,desc,ora))
            programmi[-1].printProgramma()
        #self.writeOnGuide(programmi)
        '''
        url = 'https://www.rsi.ch/palinsesto/'
        page = requests.get(url).text.split('</div><!-- /.time -->')[1].split('</div><!-- /.vectors -->')[0].replace('\n','').split('<!-- /.prog-content -->')[:-1]
        programmi = []
        for i in page:
            name = 'RSI '+re.findall(r"data-prog-vector=\"(.*?)\">",i)[0]
            info = re.findall(r"data-prog-title = \"(.*?)\"",i)[0]
            desc = re.findall(r"data-prog-description = \"(.*?)\"",i)[0]
            epis = ''
            ora = re.findall(r"data-prog-currentDay=\"(.*?)\"",i)[0] + ' ' + re.findall(r"data-prog-startTime = \"(.*?)\"",i)[0]
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