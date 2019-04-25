'''
Codifica Huffman
Scrittura in Python v2.7
2to3 e convertire in py3

'''

import math #libreria matematica
import copy #copia del vettore

#Funzioni Varie
def calcInf(dato):
    #Calcolo informazione
    return math.log(1/dato,2)

def calcEff(ent,lm):
    #calcolo efficienza
    return (ent/lm)*100

def calcLM(arr1):
    #calcolo la lunghezza media di huffman
    sm = 0
    for i in arr1:
        sm+=len(i[3])*i[1]
    return sm

def calcLMF(arr1,lung):
    #calcolo la lunghezza media fissa
    sm=0
    for i in arr1:
        sm+=i[1]*lung
    return sm

def nBitFissi(nel):
    #trovo numero di bit per la lunghezza fissa
    radq = math.sqrt(nel)
    if(str(radq).split('.')[1]!='0'):
        return int(radq)+1
    else:
        return radq

def riordVett(arr1):
    stato = 1
    tmp = 0
    #bubble sort decrescente
    for x in range(0,len(arr1)):
        stato = 0
        for j in range(len(arr1)-2,x-1,-1):
            if(arr1[j][1]<arr1[j+1][1]):
                tmp = arr1[j]
                arr1[j]=arr1[j+1]
                arr1[j+1]=tmp
                stato=1
        if(not stato):
            break
    return arr1

def cambiaVal(el1,val):
    el1[3] = val+el1[3]
    return el1

#Algoritmo di Huffman
def Huffman(arr1):
    coda = []
    orig = copy.deepcopy(arr1)
    #Faccio le varie somme e riordino il vettore arr1
    for x in range(0,len(arr1)-1):
        a=copy.deepcopy(arr1[-1])
        b=copy.deepcopy(arr1[-2])
        coda.append([a,b])
        arr1[-2][1]+=arr1[-1][1]
        arr1[-2][0]+=arr1[-1][0]
        arr1 = riordVett(arr1)[:-1]
    #assegno uno al piu probabile
    #assegno zero al meno probabile
    coda[-1][1][3]='1'
    coda[-1][0][3]='0'

    #array coda contiene tutti i passi da fare per trovare la somma delle prob(1)
    #per ogni elemento della coda dal fondo
    for i in range(0,len(coda)):
        ind = len(coda)-i-1
        for x in coda[ind]:
            for y in range(0,len(coda)):
                for z in [0,1]:
                    #guarda se ha corrispondenza col nome and se gli elementi confrontati sono diversi and la lunghezza e' magg di 0
                    if(x[0].find(coda[y][z][0])>-1 and (x[0]!=coda[y][z][0]) and len(coda[y][z][0])>0):
                        #aggiungo uno o zero in base alla corrispondenza nelle varie somme
                        coda[y][z][3]=x[3]+str(z)
 
    #porto le codifiche trovate dal vettore coda nel vettore orig
    for i in coda:
        for b in i:
            for x in orig:
                if(b[0]==x[0]):
                    x[3]=b[3]
                    break
    return orig               

#INIZIO PROGRAMMA
#Definizioni variabili
nel = 1
while(nel<=1):
    nel = input("Inserisci il numero di elementi:")
elem = []
simb = ''
entrop = 0
som = 0

#inserisco i simboli in un vettore
for i in range(0,nel):
    simb=raw_input("Inserisci il simbolo ("+str(i+1)+" el.):")
    num=-1
    while(num<0):
        num=float(input("Probabilita' in valore decimale ("+str(i+1)+" el.):"))
    som+=num
    #ogni elemento del vettore elem e' composto da un vettore di 4 elementi: simbolo,probabilita,informazione da calcolare,codifica
    elem.append([simb,num,0.0,''])
    if som >= 1:
        break #se la somma e' 1 prima di arrivare all' ultimo elemento

if int(som)==1:
    #posso eseguire
    for i in range(0,nel):
        #trovo informazione per ogni elemento
        elem[i][2]=calcInf(elem[i][1])
        #trovo entropia totale
        entrop+=elem[i][1]*elem[i][2]
        
    #trovo le codifiche e le salvo in elem dopo aver ordinato il vettore elem
    elem = Huffman(riordVett(elem))

    
    #ottengo Lunghezza media huffman e fissa
    lmv = calcLM(elem)
    lmf = calcLMF(elem,nBitFissi(nel))

    #Scrivo su file huff_encode.txt
    outfile = file('huff_encode.txt','w')
    outfile.write('Efficienza Codifica Lunghezza Variabile: '+str(calcEff(entrop,lmv))[:5]+'%\nEfficienza Codifica Lunghezza Fissa: '+str(calcEff(entrop,lmf))[:5]+'%\n\n')
    outfile.write('Lunghezza Media Codifica Variabile: '+str(lmv)[:4]+' bit\nLunghezza Media Codifica Fissa: '+str(lmf)[:4]+' bit\n\n')
    #Scrivo ogni simbolo
    for i in elem:
        outfile.write('Simbolo \''+i[0]+'\':\n\tProbabilita\': '+str(i[1])+'\n\tInformazione: '+str(i[2])[:5]+'\n\tCodifica: '+i[3]+'\n\n')
    outfile.close()
    print "Guardare file huff_encode.txt appena creato"

else:
    print "non posso eseguire, somma diversa da 1"
