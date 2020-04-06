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
dayA = [1,2,3,4,5,6] #aprile
date=[]
casi=0
tamponi=0

#out_pdf = r'/Users/marco/Desktop/image.pdf'
#pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)

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
# ITALIA - CASI PER TAMPONI E DECEDUTI
##############################################################################################################
if italiaCasiTampone == True:
    casiTampArIt=[]
    casiTampArIth24=[]
    casiTampArItLog=[]
    tamponih24=[]

    def elabCasiTampArIt(tempS,url):
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

    def calcCasiTampone(day,casi,tamponi,deceduti,mese):
        global casiTampOld
        global decedutiOld
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        ct = float( (format(round(casi/tamponi,5),'.5f')) )
        cth24 = float( (format(round( (casi-casiTampOld[0])/(tamponi-casiTampOld[1]),5),'.5f')) )
        tamponih24.append(tamponi-casiTampOld[1])
        casiTampArIt.append (ct)
        casiTampArIth24.append (cth24)
        casiTampArItLog.append( math.log10(int(casi)) )
        #date.append(datetime(year=2020, month=mese, day=d, hour = 18, minute = 30, second = 0))
        print (day + ' ' + month + ' : ', end = '')
        print (str(ct), end = '')
        print (" - casi rilevati:" + str(casi), end = '')
        print (" - tamponi effettuati:" + str(tamponi), end = '')
        print (" - rapporto ultime 24h:" + str(cth24)  )
        casiTampOld = [casi,tamponi]
        decedutiOld = deceduti

    print (f"{bcolors.WARNING}ITALIA - POSITIVI PER TAMPONI EFFETTUATI{bcolors.ENDC}")

    casiTampOld = [9172,53826] #inizializzo ai dati del 9 marzo
    decedutiOld = 1
    for d in dayM:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTampone(str(d),dat[0],dat[1],dat[2],3)
        
    for d in dayA:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-2020040')
        calcCasiTampone(str(d),dat[0],dat[1],dat[2],4)

    #plotGraph(date,casiTampArItLog,'Giorni','Casi per tamponi','Italia - Casi per tamponi (scala log.)')

    fig1, ax1 = plt.subplots()
    ax1.bar(date, tamponih24)
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

    #pdf.savefig(fig1)

##############################################################################################################
#ITALIA - TERAPIA INTENSIVA
##############################################################################################################
if italiaTerapiaIntensiva == True:
    def elabCasiTerInITA(tempS,url):
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mystrSPLIT = mystr.split(",")
        terapianIn = int(mystrSPLIT[17])  
        return terapianIn

    def calcCasiTerInITA(day,terIn,mese):
        global terInOLd
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        terInArrIt.append (terIn)
        terInArrItLog.append ( math.log10(int(terIn)) )
        diff = ( terIn - terInOLd )
        print (day + ' ' + month + ' : ' + str(terIn), end = '')
        print (" - Differenza giorno prec: " + str(diff) )
        terInOLd = terIn

    print (f"{bcolors.WARNING}ITALIA - INCREMENTO RICOVERATI TERAPIA INTENSIVA{bcolors.ENDC}" )

    terInOLd = 0
    terInArrIt=[]
    terInArrItLog=[]
    for d in dayM:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTerInITA(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-2020040')
        calcCasiTerInITA(str(d),dat,4)
        
    plotGraph(date,terInArrIt,'Giorni','Terapie Intensive','Italia - Ricoveri terapia intensiva')
    plotGraph(date,terInArrItLog,'Giorni','Terapie Intensive','Italia - Ricoveri terapia intensiva (scala log.)')

##############################################################################################################
# TOSCANA - CASI PER TAMPONI
##############################################################################################################
if toscanaCasiTampone == True:

    casiTampArTO=[]
    casiTampArTOh24=[]
    casiTampArTOLog=[]
    tamponih24TO=[]

    def elabCasiTampArTO(tempS,url):
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()
        regionSplit = mySplit[17].split(",")
        casi = int(regionSplit[15])
        tamponi = int(regionSplit[16])
        dat = [casi,tamponi]  
        return dat

    def calcCasiTampArTO(day,casi,tamponi,mese):
        global casiTampOldTO
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Aprile"
        ct = float( (format(round(casi/tamponi,5),'.5f')) )
        cth24 = float( (format(round( (casi-casiTampOldTO[0])/(tamponi-casiTampOldTO[1]),5),'.5f')) )
        tamponih24TO.append (tamponi-casiTampOldTO[1])
        casiTampArTO.append (ct)
        casiTampArTOh24.append(cth24)
        casiTampArTOLog.append( math.log10(int(casi)) )
        print (day + ' ' + month + ' : ', end = '')
        print (str(ct), end = '')
        print (" - casi rilevati: " + str(casi), end = '')
        print (" - tamponi effettuati: " + str(tamponi), end = '' )
        print (" - rapporto ultime 24h:" + str(cth24)  )
        casiTampOldTO = [casi,tamponi]

    print (f"{bcolors.WARNING}TOSCANA- POSITIVI PER TAMPONI EFFETTUATI{bcolors.ENDC}" )

    casiTampOldTO=[208,2018] #inizializzo ai dati del 9 marzo per la toscana
    for d in dayM:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTampArTO(str(d),dat[0],dat[1],3)

    for d in dayA:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-2020040')
        calcCasiTampArTO(str(d),dat[0],dat[1],4)
    
    fig2, ax1 = plt.subplots()
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

    #pdf.savefig(fig2)

##############################################################################################################
# TOSCANA - TERAPIA INTENSIVA
##############################################################################################################
if toscanaTerapiaIntensiva == True:
    def elabCasiTerInTO(tempS,url):
        data = urllib.request.urlopen(url + tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()
        regionSplit = mySplit[17].split(",")
        terapianIn = int ( regionSplit[7] )
        return terapianIn 
        
    def calcCasiTerInTO(day,terIn,mese):
        global terInOLd
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        terInTo.append (terIn)
        terInToLog.append ( math.log10(int(terIn)) )
        diff = ( terIn - terInOLd )
        print (day + ' ' + month + ' : ' + str(terIn), end = '')
        print (" - Differenza giorno prec: " + str(diff) )
        terInOLd = terIn

    print (f"{bcolors.WARNING}TOSCANA - INCREMENTO RICOVERATI TERAPIA INTENSIVA{bcolors.ENDC}" )
    terInOLd = 0
    terInTo=[]
    terInToLog=[]
    for d in dayM:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTerInTO(str(d),dat,3)

    for d in dayA:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-2020040')
        calcCasiTerInTO(str(d),dat,4)

    plotGraph(date,terInTo,'Giorni','Terapie Intensive','Toscana - Ricoveri terapia intensiva')
    plotGraph(date,terInToLog,'Giorni','Terapie Intensive','Toscana - Ricoveri terapia intensiva - Scala log')

##############################################################################################################
# PRATO - CASI
##############################################################################################################
if pratoCasi == True:
    casPo=[]
    casPoLog=[]

    def elabCasiPO(tempS,url):
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
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-2020040')
        calcCasiPO(str(d),dat,4)

    plotGraph(date,casPo,'Giorni','Casi','Prato - Casi')
    plotGraph(date,casPoLog,'Giorni','Casi','Prato - Casi (scala log.)')

##############################################################################################################
# GRAFICI COMPARATIVI
##############################################################################################################
if comparazioni == True:
    plt.plot(date,casiTampArIt)
    plt.plot(date,casiTampArTO)
    plt.ylabel("Casi")
    plt.xlabel("Giorni")
    plt.title ("Casi per tamponi - Confronto andamento Nazionale/Toscana")
    plt.show()

    plt.plot(date,casiTampArItLog)
    plt.plot(date,casiTampArTOLog)
    plt.ylabel("Casi")
    plt.xlabel("Giorni")
    plt.title ("Casi per tamponi - Confronto andamento Nazionale/Toscana (scala log)")
    plt.show() 

##############################################################################################################
#closing PDF
#pdf.close()