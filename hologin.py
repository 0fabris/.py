#!/usr/bin/python

import requests,json,sys
from datetime import datetime

class HoMobile():
    def __init__(self,ntel='',pasw=''):
        self.ntel = ntel
        self.pasw = pasw
        self.restapi = 'https://www.ho-mobile.it/leanfe/restAPI/'
        self.headers = {
            'Host':'www.ho-mobile.it',
            'Referer' : 'http://www.ho-mobile.it',
            'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
            'Accept' : '*/*'
        }

    def menu(self):
        self.ntel = sys.argv[1]
        self.pasw = sys.argv[2]
        r = self.login()
        if(r):
            print("\n\nCredito per il numero {}: {} euro.\n".format(self.ntel,self.credito()))
            self.consumi()
    def login(self):
        urlCheck = self.restapi + 'LoginService/checkAccount'
        urlLogin = self.restapi + 'LoginService/login'
        params = json.dumps({
            'channel' : 'WEB',
            'email' : None if '@' not in self.ntel else self.ntel,
            'phoneNumber': None if '@' in self.ntel else self.ntel
        })
        chkpage = requests.post(url=urlCheck,data=params,headers=self.headers)

        self.cookies = chkpage.cookies.get_dict()
        resp = json.loads(chkpage.text)

        if(resp['operationStatus']['status'] != 'OK'):
            print('Errore, utente non presente!')
            return False

        self.headers.update({'Cookie':';'.join(nome + '=' + valore for nome,valore in self.cookies.items())})

        logparams = json.dumps({
            'accountId' : resp['accountId'],
            'channel' : 'WEB',
            'email' : None if '@' not in self.ntel else self.ntel,
            'phoneNumber': None if '@' in self.ntel else self.ntel,
            'isRememberMe' : False,
            'password' : self.pasw
        })

        resplogin = json.loads(requests.post(url=urlLogin,data=logparams,headers=self.headers).text)

        if(resplogin['operationStatus']['status'] != 'OK'):
            print('Errore, login errato!')
            return False

        if '@' in self.ntel:
            self.ntel = resplogin['customerPhoneNumberList'][0]['phoneNumber']

        print('\n\t --- Benvenuto! ---\n')

        return True

    def credito(self):
        urlCredito ='https://www.ho-mobile.it/leanfe/custom/restAPI/getResidualCredit'
        self.headers['Referer'] = 'https://www.ho-mobile.it/my-account/riepilogo.html?login=success'

        params = json.dumps({
            'channel': 'WEB',
            'phoneNumber' : self.ntel
        })

        page = json.loads(requests.post(urlCredito, data=params, headers=self.headers).text)
        return page['balance']

    def consumi(self):
        urlConsumi = self.restapi + 'CountersService/getCounters'
        #print(self.headers['Cookie'])
        self.headers['Referer'] = 'https://www.ho-mobile.it/my-account/riepilogo.html?login=success'
        params = json.dumps({
            'channel' : 'WEB',
            'productId' : 1,
            'phoneNumber': str(self.ntel)
        })

        chkpage = json.loads(requests.post(url=urlConsumi,data=params,headers=self.headers).text)

        for i in chkpage['countersList']:
            print('\nL\' offerta si rinnovera\' il: {}\n'.format('/'.join(x for x in str(datetime.fromtimestamp(i['productNextRenewalDate']/1000)).split(' ')[0].split('-')[::-1])))
            for cont in i['countersDetailsList']:
                print('\n\t ---- {} ---- \n\n'.format(cont['description']) + \
                      'Residui {} {} sul totale di {} {}\n' .format(cont['residual'],cont['residualUnit'],cont['threshold'],cont['thresholdUnit'])
                      )#'Si rinnova il {}\n\n'.format(cont['nextResetDate']))

if __name__ == '__main__':
    if(len(sys.argv)!=3):
        print('\n --- Ho Mobile Login --- ' +

            '\n\n\tUtilizzo: $ hologin.py <nTelefonico/Email> <password>'+

            '\n\n - Visualizza i contatori ed il credito del numero Ho-Mobile' +
            '\n')
    else:
        HoMobile().menu()
