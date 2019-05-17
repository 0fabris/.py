'''

    0fabris
    Trenitalia Info Percorso
    Programmato durante un viaggio su un Frecciarossa
    Testato durante il viaggio

    Requisiti: requests, json
    Mi raccomando =>
        Connessione a WifiFrecce,
            anche senza essere autenticati per internet

'''

import os,requests,json,time

class TrenitaliaInfos():
    def __init__(self):
        self.urlbase = 'http://google.com/'
        self.infosurl = self.urlbase + 'infoViaggioActionJson'
        self.mapurl = self.urlbase + 'mapAction.action?width=590&height=282'
        self.timeout = 5
        while True:
            try:
                self.Infos()
            except:
                print("Mi scuso ma non riesco ad ottenere le informazioni richieste\
                        \nRiprovo tra " + str(self.timeout) + " minuti.")
            time.sleep(self.timeout)

    def Infos(self):
        os.system("clear")
        infos = json.loads(requests.get(self.infosurl).text)
        coord = [infos["lat"],infos["lon"]]
        try:
            print('\n\n\n\nBuongiorno\n\nStiamo viaggiando sul treno '+ infos["categoria"]+ ' sulla tratta "' + infos["tracktitle"].replace("&rarr;", '=>') + '", num '+ infos["tracknum"]+ \
                '\nDirezione: '+ infos["dir"]+ \
                '\nAltitudine: '+ infos["alt"] + ' m s.l.m' + \
                '\nVelocita\': '+ infos["speed"]+ " km/h" + \
                '\nLatitudine: '+ coord[0] + \
                '\nLongitudine: '+ coord[1] + \
                '\n'+ ("Ritardo di " +infos["delay"].split(' ')[1].replace('m','') + " minuti." if(infos["delay"] != '')else 'Nessun ritardo sulla linea.')  +\
                '\n')
            print('Partiti da '+ infos["trackline"]["start"]["staz"] + " alle " + infos["trackline"]["start"]["orario"]+ \
            '\nProssima fermata: '+ infos["trackline"]["mid"]["staz"] + " per l'orario " + infos["trackline"]["mid"]["orario"]+ \
            '\nFermata successiva: '+ str(infos["trackline"]["end"]["staz"]) + " per l'orario " + str(infos["trackline"]["end"]["orario"]))
            print('Progresso per la prossima fermata: {0: .2f}%'.format(infos["trackline"]["postreno"] *2))
        except:
            pass

        print("\n\tFermate della linea:")
        for i in infos["statoPercorso"]:
            print(str(i['id']+1)+ ': ' + i['description'] + (" gia passata." if i['passed'] else " non passata."))

if __name__ == '__main__':
    try:
        TrenitaliaInfos()
    except KeyboardInterrupt:
        print("\nGrazie e Arrivederci!")
