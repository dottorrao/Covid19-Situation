##############################################################################################################
#develop
##############################################################################################################

#IMPORT SECTION
import urllib.request
import os, ssl
import io
import sys
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta

##############################################################################################################
#GLOBAL VARS
dayM = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #marzo
dayA = [1,2,3,4,5,6,7,8,9,10,11] #aprile
date=[]
casi=0
tamponi=0

#out_pdf = r'/Users/marco/Desktop/image.pdf'
#pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)

## FLAG PROCESSING VARIE SEZIONI
italiaCasiTampone = True
italiaTerapiaIntensiva = True
toscanaCasiTampone = True
toscanaTerapiaIntensiva = True
pratoCasi = True
comparazioni = True

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

##############################################################################################################

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

##############################################################################################################
#GLOBAL FUN
def plotGraph(x,y,xLabel,ylabel,title):
    plt.plot(x,y)
    plt.ylabel(ylabel)
    plt.xlabel(xLabel)
    plt.title (title)
    plt.show()  

#DEFINIZIONE DEL CALENDARIO: ELENCO DEI GIORNI DA TRATTARE PER LE X DEI VARI GRAFICI
def makeCalendar():
    global date
    global dayM
    global dayA
    for d in dayM:
        date.append(datetime(year=2020, month=3, day=d, hour = 18, minute = 30, second = 0))
    for d in dayA:
        date.append(datetime(year=2020, month=4, day=d, hour = 18, minute = 30, second = 0))

##############################################################################################################

makeCalendar()

##############################################################################################################
# ITALIA - CASI PER TAMPONI - DECEDUTI
##############################################################################################################
if italiaCasiTampone == True:
    
    casiTampArIt=[]
    casiTampArIth24=[]
    casiTampArItLog=[]
    casiTampArIth24Log=[]
    tamponiIth24=[]
    casiIth24=[]
    decIt=[]
    decItLog=[]
    decedutiIth24=[]

    def elabCasiTampArIt(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url+tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mystrSPLIT = mystr.split(",")
        casi = int(mystrSPLIT[25])
        tamponi = int(mystrSPLIT[26])
        deceduti = int(mystrSPLIT[24])
        dat = [casi,tamponi,deceduti]  
        return dat

    def calcCasiTampone(day,dat,mese):
        global casiTampOld
        global decedutiOld
        global casiOld
        
        casi = dat[0]
        tamponi = dat[1]
        deceduti = dat[2]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        #casi per tamponi
        ct = float( (format(round(casi/tamponi,5),'.5f')) )
        #casi per tamponi h24
        cth24 = float( (format(round( (casi-casiTampOld[0])/(tamponi-casiTampOld[1]),5),'.5f')) )
        #decessi ultime 24h
        decIth24 = int(deceduti)-int(decedutiOld)
        #1-tamponi ultime 24h
        tamponiIth24.append(tamponi-casiTampOld[1])
        #2-casi per tampone totali array
        casiTampArIt.append ( ct ) 
        #3-casi per tampone ultime 24h
        casiTampArIth24.append ( cth24 )
        #4-casi per tampone ultime 24h logaritmica
        casiTampArIth24Log.append ( math.log10(cth24) )
        #5-casi per tampone totali logaritmica
        casiTampArItLog.append( math.log10(int(casi)) )
        #6-casi ultime 24h
        casiIth24.append ( int(casi)-int(casiOld) ) 
        #7-deceduti ultime 24h
        decedutiIth24.append ( decIth24 )
        #8-deceduti totali
        decIt.append (deceduti)  
        #9-deceduti totali logaritmica
        decItLog.append ( math.log10( deceduti ) )

        #print dei dati su terminale
        print (day + ' ' + month + ' : ', end = '')
        print (str(ct), end = '')
        print (" - casi rilevati:" + str(casi), end = '')
        print (" - tamponi effettuati:" + str(tamponi), end = '')
        print (" - rapporto ultime 24h:" + str(cth24), end = ''  )
        print (" - decessi ultime 24h:" + str(decIth24) )
        
        #salvataggio valori appena processati per differenza giorno precedente
        casiTampOld = [casi,tamponi]
        casiOld = casi
        decedutiOld = deceduti
        
    print (f"{bcolors.WARNING}ITALIA - POSITIVI PER TAMPONI EFFETTUATI{bcolors.ENDC}")

    #variabili per salvataggio valori giorno precedente
    casiTampOld = [9172,53826]  #inizializzo ai dati del 9 marzo
    casiOld = 9172              #inizializzo ai dati del 9 marzo
    decedutiOld = 1             #da inizializzare ai dati del 9 marzo

    for d in dayM:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTampone(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
        calcCasiTampone(str(d),dat,4)

    ## GRAFICI ##

    #1-Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h
    fig10, ax1 = plt.subplots()
    ax1.bar(date, tamponiIth24)
    ax1.legend(labels=['Tamponi giornalieri'])
    ax2 = ax1.twinx()
    ax2.plot(date, casiTampArIth24,color='tab:orange')
    ax2.plot(date, casiTampArIt,color='tab:red')
    ax2.legend(labels=['Casi/Tamponi h24', 'Casi/Tamponi da inizio'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h')
    ax2.set(xlabel='Giorni', ylabel='Casi per tampone',
        title='Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h')
    ax1.grid()
    plt.show()

    #2-Casi per tamponi Italia - Bubble chart giorni/tamponi/casi
    size = [n/2 for n in casiIth24]
    fig20, ax1 = plt.subplots()
    ax1.scatter(date, tamponiIth24, color='red', s=size, alpha=0.3, edgecolors='black')
    ax1.legend(labels=['Casi giornalieri'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Italia - Bubble chart giorni/tamponi/casi')
    ax1.grid()
    plt.show()

    #3-Italia - Casi per tamponi (scala log.)
    fig30, ax1 = plt.subplots()
    ax1.plot(date, casiTampArItLog)
    ax1.set(xlabel='Giorni', ylabel='Casi per tamponi',
        title='Italia - Casi per tamponi (scala log.)')
    ax1.grid()
    plt.show()

    #4-Italia - Decessi ultime 24h
    fig31, ax1 = plt.subplots()
    ax1.bar(date, decedutiIth24)
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Italia - Decessi ultime 24h')
    ax1.grid()
    plt.show()

    #5-Italia - Decessi totale (scala log)
    fig32, ax1 = plt.subplots()
    ax1.bar(date, decItLog)
    ax1.plot(date, decItLog, color='tab:orange')
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Italia - Decessi totale (scala log)')
    ax1.grid()
    plt.show()

##############################################################################################################
# TOSCANA - CASI PER TAMPONI - DECEDUTI
##############################################################################################################
if toscanaCasiTampone == True:

    casiTampArTO=[]
    casiTampArTOh24=[]
    casiTampArTOLog=[]
    tamponih24TO=[]
    casih24TO=[]
    decTO=[]
    dech24TO=[]
    decTOLog=[]

    def elabCasiTampArTO(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()
        regionSplit = mySplit[17].split(",")
        casi = int(regionSplit[15])
        tamponi = int(regionSplit[16])
        decessi = int(regionSplit[14])
        dat = [casi,tamponi,decessi]  
        return dat

    def calcCasiTampArTO(day,dat,mese):
        global casiTampOldTO
        global casiOldTO
        global decessiOld
        casi=dat[0]
        tamponi=dat[1]
        decessi=dat[2]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Aprile"
        ct = float( (format(round(casi/tamponi,5),'.5f')) )
        cth24 = float( (format(round( (casi-casiTampOldTO[0])/(tamponi-casiTampOldTO[1]),5),'.5f')) )
        #1-tamponi ultime 24h
        tamponih24TO.append (tamponi-casiTampOldTO[1])
        #2-casi/tamponi totale
        casiTampArTO.append (ct)
        #3-casi/tampone ultime 24h
        casiTampArTOh24.append(cth24)
        #4-casi/tampone logaritmica
        casiTampArTOLog.append( math.log10(int(casi)) )
        #5-casi ultime 24h
        casih24TO.append ( int(casi)-int(casiOldTO) ) 
        #6-decessi ultime 24h
        decessih24 = decessi - decessiOld
        #7-decessi totale
        decTO.append (decessi)
        #8-decessi ultime 24h
        dech24TO.append (decessih24)
        #9-decessi logaritmica
        decTOLog.append ( math.log10(int(decessi) ) )

        #print dei dati su terminale
        print (day + ' ' + month + ' : ', end = '')
        print (str(ct), end = '')
        print (" - casi rilevati:" + str(casi), end = '')
        print (" - tamponi effettuati:" + str(tamponi), end = '')
        print (" - rapporto ultime 24h:" + str(cth24), end = ''  )
        print (" - decessi ultime 24h:" + str(decessih24) )

        casiTampOldTO = [casi,tamponi]
        casiOldTO = casi
        decessiOld = decessi

    print (f"{bcolors.WARNING}TOSCANA- POSITIVI PER TAMPONI EFFETTUATI{bcolors.ENDC}" )

    casiTampOldTO = [208,2018]  #inizializzo ai dati del 9 marzo per la toscana
    casiOldTO = 1               #da inizializzare
    decessiOld = 1              #da inizializzare
    for d in dayM:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTampArTO(str(d),dat,3)

    for d in dayA:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTampArTO(str(d),dat,4)
    
    #1 - Casi per tampone Toscana
    fig60, ax1 = plt.subplots()
    ax1.bar(date, tamponih24TO)
    ax1.legend(labels=['Tamponi giornalieri'])
    ax2 = ax1.twinx()
    ax2.plot(date, casiTampArTOh24,color='tab:orange')
    ax2.plot(date, casiTampArTO,color='tab:red')
    ax2.legend(labels=['Casi/Tamponi h24', 'Casi/Tamponi da inizio'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Toscana - Confronto andamento inizio epidemia/giornaliero ultime 24h')
    ax2.set(xlabel='Giorni', ylabel='Casi per tampone',
        title='Casi per tamponi Toscana - Confronto andamento inizio epidemia/giornaliero ultime 24h')
    ax1.grid()
    plt.show()
    
    #2 - Casi per tamponi Toscana - Bubble chart giorni/tamponi/casi
    size = [n*7 for n in casih24TO]
    fig70, ax1 = plt.subplots()
    ax1.scatter(date, tamponih24TO, color='red', s=size, alpha=0.3, edgecolors='black')
    ax1.legend(labels=['Casi giornalieri'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Toscana - Bubble chart giorni/tamponi/casi')
    ax1.grid()
    plt.show()

    #3 - Toscana - Decessi ultime 24h
    fig71, ax1 = plt.subplots()
    ax1.bar(date, dech24TO)
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Toscana - Decessi ultime 24h')
    ax1.grid()
    plt.show()

    #4 - Toscana - Decessi totali (scala log)
    fig72, ax1 = plt.subplots()
    ax1.bar(date, decTOLog)
    ax1.plot(date, decTOLog, color='tab:orange')
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Toscana - Decessi totali (scala log)')
    ax1.grid()
    plt.show()

##############################################################################################################
#ITALIA - OSPEDALIZZATI
##############################################################################################################
if italiaTerapiaIntensiva == True:
    def elabCasiTerInITA(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mystrSPLIT = mystr.split(",")
        terapianIn = int(mystrSPLIT[17])
        ricoverati = int(mystrSPLIT[16])   
        return [ricoverati,terapianIn]

    def calcCasiTerInITA(day,dat,mese):
        global terInOLd
        global ricoverati
        ricov=dat[0]
        terIn=dat[1]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        terInArrIt.append (terIn)
        ricoverati.append (ricov)
        terInArrItLog.append ( math.log10(int(terIn)) )
        diff = ( terIn - terInOLd )
        print (day + ' ' + month + ' : ' + 'Ricoverati con sintomi:' + str(ricov), end = '')
        print (' - Terapia intensiva: ' + str(terIn), end = '')
        print (' - Incr.Terapia Intensiva: ' + str(diff) )
        terInOLd = terIn

    print (f"{bcolors.WARNING}ITALIA - OSPEDALIZZATI{bcolors.ENDC}" )

    terInOLd = 0
    terInArrIt=[]
    ricoverati=[]
    terInArrItLog=[]
    for d in dayM:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTerInITA(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
        calcCasiTerInITA(str(d),dat,4)
    
    fig40, ax1 = plt.subplots()
    ax1.plot(date, terInArrIt)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Italia - Ricoveri terapia intensiva')
    ax1.grid()
    plt.show()

    fig50, ax1 = plt.subplots()
    ax1.plot(date, terInArrItLog)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Italia - Ricoveri terapia intensiva (scala log.)')
    ax1.grid()
    plt.show()

    p51 = plt.bar(date, ricoverati)
    p52 = plt.bar(date, terInArrIt, bottom = ricoverati)
    plt.legend(['Ricoverati','Terapia Intensiva'])
    plt.xlabel('Giorni') 
    plt.ylabel('Totale ospedalizzati') 
    plt.title('Italia - Totale ospedalizzati')
    plt.grid()
    plt.show()

##############################################################################################################
# TOSCANA - OSPEDALIZZATI
##############################################################################################################
if toscanaTerapiaIntensiva == True:
    def elabCasiTerInTO(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()
        regionSplit = mySplit[17].split(",")
        terapianIn = int (regionSplit[7])
        ricoverati = int(regionSplit[8])
        return [terapianIn,ricoverati]
        
    def calcCasiTerInTO(day,dat,mese):
        global terInOLd
        global ricoveratiTO
        terIn = dat[0]
        ricoverati = dat[1]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        terInTo.append (terIn)
        terInToLog.append ( math.log10(int(terIn)) )
        ricoveratiTO.append (ricoverati)
        diff = ( terIn - terInOLd )
        #print (day + ' ' + month + ' : ' + str(terIn), end = '')
        #print (" - Differenza giorno prec: " + str(diff) )
        print (day + ' ' + month + ' : ' + 'Ricoverati con sintomi:' + str(ricoverati), end = '')
        print (' - Terapia intensiva: ' + str(terIn), end = '')
        print (' - Incr.Terapia Intensiva: ' + str(diff) )
        terInOLd = terIn

    print (f"{bcolors.WARNING}TOSCANA - INCREMENTO RICOVERATI TERAPIA INTENSIVA{bcolors.ENDC}" )
    terInOLd = 0
    terInTo=[]
    terInToLog=[]
    ricoveratiTO=[]
    for d in dayM:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTerInTO(str(d),dat,3)

    for d in dayA:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTerInTO(str(d),dat,4)

    fig80, ax1 = plt.subplots()
    ax1.plot(date, terInTo)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Toscana - Ricoveri terapia intensiva')
    ax1.grid()
    plt.show()

    fig90, ax1 = plt.subplots()
    ax1.plot(date, terInToLog)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Toscana - Ricoveri terapia intensiva - Scala log')
    ax1.grid()
    plt.show()

    p91 = plt.bar(date, ricoveratiTO)
    p92 = plt.bar(date, terInTo, bottom = ricoveratiTO) 
    plt.legend(['Ricoverati','Terapia Intensiva'])
    plt.xlabel('Giorni') 
    plt.ylabel('Totale ospedalizzati') 
    plt.title('Toscana - Totale ospedalizzati')
    plt.grid()
    plt.show()

##############################################################################################################
# PRATO - CASI
##############################################################################################################
if pratoCasi == True:
    casPo=[]
    casPoLog=[]

    def elabCasiPO(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url+tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()
        poRowSplit = mySplit[111].split(',')
        if poRowSplit[9] == '':
            casi = 0
        else:
            casi = int(poRowSplit[9])
        return casi

    def calcCasiPO(day,casi,mese):
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Aprile" 

        casPo.append (casi)

        if casi == 0:
            casPoLog.append( 0 )
        else:
            casPoLog.append( math.log10(int(casi)) )
        
        print (day + ' ' + month + ' : ', end = '')
        print (" - casi rilevati:" + str(casi) )

    print (f"{bcolors.WARNING}PRATO - CASI{bcolors.ENDC}" )

    for d in dayM:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202003')
        calcCasiPO(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202004')
        calcCasiPO(str(d),dat,4)

    fig90, ax1 = plt.subplots()
    ax1.plot(date, casPo)
    ax1.set(xlabel='Giorni', ylabel='Casi',
        title='Prato - Casi - Scala log')
    ax1.grid()
    plt.show()

    fig100, ax1 = plt.subplots()
    ax1.plot(date, casPoLog)
    ax1.set(xlabel='Giorni', ylabel='Casi',
        title='Prato - Casi - Scala log')
    ax1.grid()
    plt.show()

##############################################################################################################
# GRAFICI COMPARATIVI
##############################################################################################################
if comparazioni == True:
    
    fig110, ax1 = plt.subplots()
    ax1.plot(date, casiTampArIt)
    ax1.plot(date, casiTampArTO)
    ax1.set(xlabel='Giorni', ylabel='Casi',
        title='Casi per tamponi - Confronto andamento Nazionale/Toscana')
    ax1.grid()
    plt.show()
    
    fig120, ax1 = plt.subplots()
    ax1.plot(date, casiTampArItLog)
    ax1.plot(date, casiTampArTOLog)
    ax1.set(xlabel='Giorni', ylabel='Casi',
        title='Casi per tamponi - Confronto andamento Nazionale/Toscana (scala log)')
    ax1.grid()
    plt.show()

##############################################################################################################
#closing PDF
#pdf.close()