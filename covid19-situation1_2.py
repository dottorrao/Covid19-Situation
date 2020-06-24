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
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
from PIL import Image
from matplotlib.dates import date2num

##############################################################################################################
#GLOBAL VARS
dayM = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #marzo
dayA = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] #aprile
dayMay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #maggio
dayJun = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]#Giugno
date=[]
casi=0
tamponi=0
regione = ""

#out_pdf = r'/Users/marco/Desktop/image.pdf'
#pdf = matplotlib.backends.backend_pdf.PdfPages(out_pdf)

## FLAG PROCESSING VARIE SEZIONI
italiaCasiTampone = True
italiaTerapiaIntensiva = True
toscanaCasiTampone = True
toscanaTerapiaIntensiva = True
pratoCasi = True
comparazioni = False

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
    #plt.show()  

#DEFINIZIONE DEL CALENDARIO: ELENCO DEI GIORNI DA TRATTARE PER LE X DEI VARI GRAFICI
def makeCalendar():
    global date
    global dayM
    global dayA
    global dayM
    for d in dayM:
        date.append(datetime(year=2020, month=3, day=d, hour = 18, minute = 30, second = 0))
    for d in dayA:
        date.append(datetime(year=2020, month=4, day=d, hour = 18, minute = 30, second = 0))
    for d in dayMay:
        date.append(datetime(year=2020, month=5, day=d, hour = 18, minute = 30, second = 0))
    for d in dayJun:
        date.append(datetime(year=2020, month=6, day=d, hour = 18, minute = 30, second = 0))

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
        casi = int(mystrSPLIT[26])
        tamponi = int(mystrSPLIT[27])
        deceduti = int(mystrSPLIT[25])
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
        elif mese == 5:
            month = "Maggio" 
        elif mese == 6:
            month = "Giugno" 
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
        print (" - casi h24:" + str( int(casi)-int(casiOld) ), end = '' )
        print (" - tamponi effettuati:" + str(tamponi), end = '')
        print (" - tamponi h24:" + str(tamponi-casiTampOld[1]), end = '')
        print (" - rapporto giornaliero:" + str(cth24), end = ''  )
        print (" - decessi giornlieri:" + str(decIth24) )
        
        #salvataggio valori appena processati per differenza giorno precedente
        casiTampOld = [casi,tamponi]
        casiOld = casi
        decedutiOld = deceduti
        
    print (f"{bcolors.WARNING}ITALIA - POSITIVI PER TAMPONI / DECESSI GIORNALIERI{bcolors.ENDC}")

    #variabili per salvataggio valori giorno precedente
    casiTampOld = [9172,53826]  #inizializzo ai dati del 9 marzo
    casiOld = 9172              #inizializzo ai dati del 9 marzo
    decedutiOld = 463           #da inizializzare ai dati del 9 marzo

    for d in dayM:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTampone(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
        calcCasiTampone(str(d),dat,4)
    
    for d in dayMay:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202005')
        calcCasiTampone(str(d),dat,5)

    for d in dayJun:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202006')
        #correzione casi rilevari
        if ( d >= 12 ):
            dat[0]=dat[0]+230
        if ( d >= 19):
            dat[0]=dat[0]+397
            dat[0]=dat[0]+2
        calcCasiTampone(str(d),dat,6)

    ## GRAFICI ##

    #1-Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h
    fig10, ax1 = plt.subplots()
    ax1.bar(date, tamponiIth24)
    ax1.legend(labels=['Tamponi giornalieri'])
    ax2 = ax1.twinx()
    ax2.plot(date, casiTampArIth24,color='tab:orange',linewidth=3)
    ax2.plot(date, casiTampArIt,color='tab:red',linewidth=3)
    ax2.legend(labels=['Casi/Tamponi h24', 'Casi/Tamponi da inizio'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero')
    ax2.set(xlabel='Giorni', ylabel='Casi per tampone',
        title='Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Casi_per_tamponi_Italia.png') 
    #plt.show()

    #2-Casi per tamponi Italia - Bubble chart giorni/tamponi/casi
    size = [n/2 for n in casiIth24]
    fig20, ax1 = plt.subplots()
    ax1.scatter(date, tamponiIth24, color='red', s=size, alpha=0.3, edgecolors='black')
    ax1.legend(labels=['Casi giornalieri'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Italia - Bubble chart giorni/tamponi/casi')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ##plt.show()

    '''
    #3-Italia - Casi per tamponi (scala log.)
    fig30, ax1 = plt.subplots()
    ax1.plot(date, casiTampArItLog)
    ax1.set(xlabel='Giorni', ylabel='Casi per tamponi',
        title='Italia - Casi per tamponi (scala log.)')
    ax1.grid()
    #plt.show()
    '''

    #4-Italia - Decessi ultime 24h
    fig31, ax1 = plt.subplots()
    ax1.bar(date, decedutiIth24)
    ax1.plot(date, decedutiIth24, color="red")
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Italia - Decessi giorno')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Decessi_24h_Italia.png') 
    #plt.show()

    #5-Italia - Decessi totale (scala log)
    fig32, ax1 = plt.subplots()
    ax1.bar(date, decItLog)
    ax1.plot(date, decItLog, color='tab:orange')
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Italia - Decessi totale (scala log)')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    #plt.show()

##############################################################################################################
# TOSCANA - POSITIVI PER TAMPONI
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
        #regionSplit = mySplit[10].split(",") #lombardia
        regionSplit = mySplit[17].split(",") #toscana
        #regionSplit = mySplit[21].split(",") #veneto
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
        elif mese == 5:
            month = "Maggio"
        elif mese == 6:
            month = "Giugno"
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
        print (" - casi rilevati h24:" + str( int(casi)-int(casiOldTO) ), end = '')
        print (" - tamponi effettuati:" + str(tamponi), end = '')
        print (" - tamponi effettuati h24:" + str( tamponi-casiTampOldTO[1] ), end = '')
        print (" - rapporto giornaliero:" + str(cth24), end = '')
        print (" - decessi giornalieri:" + str(decessih24) )

        casiTampOldTO = [casi,tamponi]
        casiOldTO = casi
        decessiOld = decessi

    print (f"{bcolors.WARNING}TOSCANA - POSITIVI PER TAMPONI / DECESSI GIORNALIERI{bcolors.ENDC}" )

    casiTampOldTO = [208,2018]  #inizializzo ai dati del 9 marzo per la toscana
    casiOldTO = 1               #da inizializzare
    decessiOld = 1              #da inizializzare
    for d in dayM:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTampArTO(str(d),dat,3)

    for d in dayA:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTampArTO(str(d),dat,4)
    
    for d in dayMay:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202005')
        calcCasiTampArTO(str(d),dat,5)
    
    for d in dayJun:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202006')
        calcCasiTampArTO(str(d),dat,6)

    #1 - Casi per tampone Toscana
    fig60, ax1 = plt.subplots()
    ax1.bar(date, tamponih24TO)
    ax1.legend(labels=['Tamponi giornalieri'])
    ax2 = ax1.twinx()
    ax2.plot(date, casiTampArTOh24,color='tab:orange',linewidth=3)
    ax2.plot(date, casiTampArTO,color='tab:red',linewidth=3)
    ax2.legend(labels=['Casi/Tamponi h24', 'Casi/Tamponi da inizio'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Toscana - Confronto andamento inizio epidemia/giornaliero')
    ax2.set(xlabel='Giorni', ylabel='Casi per tampone',
        title='Casi per tamponi Toscana - Confronto andamento inizio epidemia/giornaliero')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Casi_per_tamponi_Toscana.png') 
    ##plt.show()
    
    #2 - Casi per tamponi Toscana - Bubble chart giorni/tamponi/casi
    size = [n*7 for n in casih24TO]
    fig70, ax1 = plt.subplots()
    ax1.scatter(date, tamponih24TO, color='red', s=size, alpha=0.3, edgecolors='black')
    ax1.legend(labels=['Casi giornalieri'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Toscana - Bubble chart giorni/tamponi/casi')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    #plt.show()

    #3 - Toscana - Decessi ultime 24h
    fig71, ax1 = plt.subplots()
    ax1.bar(date, dech24TO)
    ax1.plot(date, dech24TO, color="red")
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Toscana - Decessi giornalieri')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Decessi_24h_Toscana.png')
    #plt.show()

    #4 - Toscana - Decessi totali (scala log)
    fig72, ax1 = plt.subplots()
    ax1.bar(date, decTOLog)
    ax1.plot(date, decTOLog, color='tab:orange')
    ax1.set(xlabel='Giorni', ylabel='Deceduti',
        title='Toscana - Decessi totali (scala log)')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    #plt.show()

##############################################################################################################
#ITALIA - OSPEDALIZZATI/DIMESSI
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
        terapianIn = int(mystrSPLIT[18])
        ricoverati = int(mystrSPLIT[17])
        dimessi = int(mystrSPLIT[24])   
        return [ricoverati,terapianIn,dimessi]

    def calcCasiTerInITA(day,dat,mese):
        global terInOLd
        global ricoverati
        global dimessiIt
        global ospedalizzatiOld
        global terItOLd
        global dimessiItOld
        ricov=dat[0]
        terIn=dat[1]
        dimessi=dat[2]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        elif mese == 5:
            month = "Maggio" 
        elif mese == 6:
            month = "Giugno" 
        terInArrIt.append (terIn)
        ricoverati.append (ricov)
        terInArrItLog.append ( math.log10(int(terIn)) )
        ospedalizzatiIt.append (terIn+ricov)
        ospedalizzatiIth24.append ( terIn+ricov-ospedalizzatiOld )
        dimessiIt.append(dimessi)
        dimessiItLog.append ( math.log10(int(dimessi)) ) 
        ospedalizzatiItLog.append ( math.log10(int(terIn+ricov))  )
        dimessiIth24.append(dimessi-dimessiItOld)
        diff = ( terIn - terInOLd )
        terInArrIth24.append (diff)
        print (day + ' ' + month + ' : ' + 'Ricoverati con sintomi:' + str(ricov), end = '')
        print (' - Terapia intensiva: ' + str(terIn), end = '')
        print (' - Totale ospedalizzati: ' + str(terIn+ricov), end = '')
        print (' - Dimessi: ' + str(dimessi), end = '')
        print (' - Incr.Terapia Intensiva: ' + str(diff) )
        terInOLd = terIn
        ospedalizzatiOld = terIn+ricov
        dimessiItOld = dimessi

    print (f"{bcolors.WARNING}ITALIA - OSPEDALIZZATI/DIMESSI{bcolors.ENDC}" )

    terInOLd = 0
    ospedalizzatiOld = 5049
    terInArrIt=[]
    ricoverati=[]
    terInArrItLog=[]
    ospedalizzatiIt=[]
    ospedalizzatiIth24=[]
    dimessiIt=[]
    dimessiItLog=[]
    ospedalizzatiItLog=[]
    dimessiIth24=[]
    terInArrIth24=[]
    dimessiItOld = 724

    for d in dayM:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTerInITA(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
        calcCasiTerInITA(str(d),dat,4)
    
    for d in dayMay:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202005')
        calcCasiTerInITA(str(d),dat,5)
     
    for d in dayJun:
        dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202006')
        calcCasiTerInITA(str(d),dat,6)

    #Italia - Ricoveri terapia intensiva
    fig40, ax1 = plt.subplots()
    ax1.plot(date, terInArrIt)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Italia - Ricoveri terapia intensiva')
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    #plt.show()

    #Italia - Ricoveri terapia intensiva (scala log.)
    fig50, ax1 = plt.subplots()
    ax1.plot(date, terInArrItLog)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Italia - Ricoveri terapia intensiva (scala log.)')
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    #plt.show()

    #Italia - Totale ospedalizzati
    fig51, ax1 = plt.subplots()
    ax1.bar(date, ricoverati, color="orange")
    ax1.bar(date, terInArrIt, color="purple")
    ax1.bar(date, dimessiIt, bottom = ricoverati, color="green")
    ax1.set(xlabel='Giorni', ylabel='Totale ospedalizzati/Dimessi',
        title='Italia - Totale ospedalizzati')
    ax1.legend(labels=['Ricoverati con sintomi','Terapia Intensiva','Dimessi'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/Totale_Ospedalizzati_Italia.png')
    #plt.show()

    #Italia - Deceduti/Dimessi/Ospedalizzati
    fig52, ax1 = plt.subplots()
    ax1.plot(date, decIt, color="black")
    #ax1.plot(date, dimessiIt, color="green")
    ax1.plot(date, ospedalizzatiIt, color="orange")
    ax1.plot(date, terInArrIt, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Italia - Deceduti/Dimessi/Ospedalizzati Totali')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.legend(labels=['Deceduti', 'Ospedalizzati', 'Terapie Intensive'])
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Italia.png')
    #plt.show()

    #Italia - Deceduti/Dimessi/Ospedalizzati ultime 24h
    fig53, ax1 = plt.subplots()
    ax1.plot(date, decedutiIth24, color="black")
    #ax1.plot(date, dimessiIth24, color="green")
    ax1.plot(date, ospedalizzatiIth24, color="orange")
    ax1.plot(date, terInArrIth24, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Italia - Deceduti/Dimessi/Ospedalizzati variazione giornaliera')
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    ax1.legend(labels=['Deceduti', 'Ospedalizzati', 'Terapie Int.'])
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Italia_VARH24.png')
    #plt.show()

    #Italia - Deceduti/Dimessi/Ospedalizzati Logaritmica
    yticks = [0, 560, 1000, 1778, 3162, 5623, 10000, 17782, 31622]
    fig54, ax1 = plt.subplots()
    ax1.plot(date, decItLog, color="black")
    ax1.plot(date, dimessiItLog, color="green")
    ax1.plot(date, ospedalizzatiItLog, color="orange")
    ax1.plot(date, terInArrItLog, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Italia - Deceduti/Dimessi/Ospedalizzati logaritmica')
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.set_yticklabels(["$%.1f$" % y for y in yticks])
    ax1.grid()
    ax1.legend(labels=['Deceduti', 'Dimessi', 'Ospedalizzati', 'Terapie Int.'])
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Italia_LOG.png')
    #plt.show()

    #Italia - Terapie intensive
    fig51, ax1 = plt.subplots()
    ax1.bar(date, terInArrIt, color="purple")
    ax1.set(xlabel='Giorni', ylabel='Terapi Intensive',
        title='Italia - Totale Terapie Intensive')
    ax1.legend(labels=['Terapie Intensive'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/Terapie_Intensive_Italia.png')
    #plt.show()

    #6-Italia - Decessi giornalieri VS ospedalizzati 15gg precedenti
    decLast10days = decedutiIth24[(len(decedutiIth24)-15):(len(decedutiIth24))]
    ospPast = ospedalizzatiIt[(len(ospedalizzatiIt)-30):(len(ospedalizzatiIt)-15)] 
    #last10day = date[(len(date)-10):(len(date))]
    fig52, ax1 = plt.subplots()
    ax1.bar(date2num( date[(len(date)-15):(len(date))] )-0.4, ospPast, color="orange", align="center", width=0.4)
    ax2 = ax1.twinx()
    ax2.bar(date2num( date[(len(date)-15):(len(date))] ), decLast10days, color="gray", align="center", width=0.4)
    ax1.set(xlabel='Giorni', ylabel='Ospedalizzati 15gg precedenti', title='Italia - Deceduti giornalieri rispetto ospedalizzati 15gg precedenti')
    ax2.set(xlabel='Giorni', ylabel='Deceduti', title='')
    ax1.legend(labels=['Ospedalizzati'])
    ax2.legend(labels=['Deceduti'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/DecedutiGioVSOsped15gpast_ITA.png')
    #plt.show()


##############################################################################################################
# TOSCANA - OSPEDALIZZATI/DIMESSI
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
        
        regionSplit = mySplit[17].split(",") #toscana
        #regionSplit = mySplit[10].split(",") #lombardia

        terapianIn = int (regionSplit[7])
        ricoverati = int(regionSplit[8])
        dimessi = int(regionSplit[13])
        return [terapianIn,ricoverati,dimessi]
        
    def calcCasiTerInTO(day,dat,mese):
        global terInOLd
        global ricoveratiTO
        global dimessiTO
        global ospedalizzatiTO
        global ospedalizzatiTOh24
        global dimessiTOh24
        global ospedalizzatiTOOld
        global dimessiTOOld
        terIn = dat[0]
        ricoverati = dat[1]
        dimessi = dat[2]
        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Arile" 
        elif mese == 5:
            month = "Maggio" 
        elif mese == 6:
            month = "Giugno" 
        terInTo.append (terIn)
        terInToLog.append ( math.log10(int(terIn)) )
        ricoveratiTO.append (ricoverati)
        dimessiTO.append (dimessi)
        dimessiTOlog.append ( math.log10(int(dimessi)) )
        ospedalizzatiTO.append (ricoverati+terIn)
        ospedalizzatiTOLog.append ( math.log10(int(ricoverati+terIn)) ) 
        diff = ( terIn - terInOLd )
        terInArrToh24.append (diff)
        ospedalizzatiTOh24.append (ricoverati+terIn-ospedalizzatiTOOld)
        dimessiTOh24.append (dimessi-dimessiTOOld)
        #print (day + ' ' + month + ' : ' + str(terIn), end = '')
        #print (" - Differenza giorno prec: " + str(diff) )
        print (day + ' ' + month + ' : ' + 'Ricoverati con sintomi:' + str(ricoverati), end = '')
        print (' - Terapia intensiva: ' + str(terIn), end = '')
        print (' - Totale ospedalizzati: ' + str(terIn+ricoverati), end = '')
        print (' - Dimessi: ' + str(dimessi), end = '')
        print (' - Incr.Terapia Intensiva: ' + str(diff) )
        terInOLd = terIn
        ospedalizzatiTOOld = ricoverati+terIn
        dimessiTOOld = dimessi
    
    print (f"{bcolors.WARNING}TOSCANA- OSPEDALIZZATI/DIMESSI{bcolors.ENDC}" )
    
    terInOLd = 0
    terInTo=[]
    terInToLog=[]
    ricoveratiTO=[]
    dimessiTO=[]
    ospedalizzatiTO=[]
    ospedalizzatiTOh24=[]
    dimessiTOh24=[]
    ospedalizzatiTOOld=0
    dimessiTOOld=0
    terInArrToh24=[]
    dimessiTOlog=[]
    ospedalizzatiTOLog=[]


    for d in dayM:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTerInTO(str(d),dat,3)

    for d in dayA:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTerInTO(str(d),dat,4)
    
    for d in dayMay:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202005')
        calcCasiTerInTO(str(d),dat,5)
     
    for d in dayJun:
        dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202006')
        calcCasiTerInTO(str(d),dat,6)

    fig80, ax1 = plt.subplots()
    ax1.plot(date, terInTo)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Toscana - Ricoveri terapia intensiva')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    #plt.show()

    fig90, ax1 = plt.subplots()
    ax1.plot(date, terInToLog)
    ax1.set(xlabel='Giorni', ylabel='Terapie Intensive',
        title='Toscana - Ricoveri terapia intensiva - Scala log')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    #plt.show()

    fig91, ax1 = plt.subplots()
    ax1.bar(date, ricoveratiTO, color="orange")
    ax1.bar(date, terInTo, color="purple")
    ax1.bar(date, dimessiTO, bottom = ricoveratiTO, color="green")
    ax1.set(xlabel='Giorni', ylabel='Totale ospedalizzati',
        title='Toscana - Totale ospedalizzati')
    ax1.legend(labels=['Ricoverati con sintomi','Terapia Intensiva','Dimessi'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/Totale_Ospedalizzati_Toscana.png')
    #plt.show()

    #Toscana - Deceduti/Dimessi/Ospedalizzati
    fig92, ax1 = plt.subplots()
    ax1.plot(date, decTO, color="black")
    #ax1.plot(date, dimessiTO, color="green")
    ax1.plot(date, ospedalizzatiTO, color="orange")
    ax1.plot(date, terInTo, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Toscana - Deceduti/Dimessi/Ospedalizzati Totali')
    ax1.grid()
    ax1.legend(labels=['Deceduti', 'Ospedalizzati', 'Terapie Intensive'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana.png')
    #plt.show()

    #Toscana - Deceduti/Dimessi/Ospedalizzati giornalieri
    fig93, ax1 = plt.subplots()
    ax1.plot(date, dech24TO, color="black")
    #ax1.plot(date, dimessiTOh24, color="green")
    ax1.plot(date, ospedalizzatiTOh24, color="orange")
    ax1.plot(date, terInArrToh24, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Toscana - Deceduti/Dimessi/Ospedalizzati variazione giornalieri')
    ax1.grid()
    ax1.legend(labels=['Deceduti', 'Ospedalizzati', 'Terapie Intensive'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana_VARH24.png')
    #plt.show()

    
    #Toscana - Deceduti/Dimessi/Ospedalizzati Logaritmica
    fig94, ax1 = plt.subplots()
    yticks = [0, 1, 3, 10, 31, 100, 316, 1000]
    ax1.plot(date, decTOLog, color="black")
    ax1.plot(date, dimessiTOlog, color="green")
    ax1.plot(date, ospedalizzatiTOLog, color="orange")
    ax1.plot(date, terInToLog, color="purple")
    ax1.set(xlabel='Giorni', ylabel='',
        title='Toscana - Deceduti/Dimessi/Ospedalizzati logaritmica')
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.set_yticklabels(["$%.1f$" % y for y in yticks])
    ax1.grid()
    ax1.legend(labels=['Deceduti', 'Dimessi', 'Ospedalizzati', 'Terapie Int.'])
    plt.savefig('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana_LOG.png')
    #plt.show()

    #Toscana - Terapie intensive
    fig51, ax1 = plt.subplots()
    ax1.bar(date, terInTo, color="purple")
    ax1.set(xlabel='Giorni', ylabel='Terapi Intensive',
        title='Toscana - Totale Terapie Intensive')
    ax1.legend(labels=['Terapie Intensive'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/Terapie_Intensive_Toscana.png')
    #plt.show()

    #6-Toscana - Decessi giornalieri VS ospedalizzati 15gg precedenti
    decLast10days = dech24TO[(len(dech24TO)-15):(len(dech24TO))]
    ospPast = ospedalizzatiTO[(len(ospedalizzatiTO)-30):(len(ospedalizzatiTO)-15)] 
    #last10day = date[(len(date)-10):(len(date))]
    fig52, ax1 = plt.subplots()
    ax1.bar(date2num( date[(len(date)-15):(len(date))] )-0.4, ospPast, color="orange", align="center", width=0.4)
    ax2 = ax1.twinx()
    ax2.bar(date2num( date[(len(date)-15):(len(date))] ), decLast10days, color="gray", align="center", width=0.4)
    ax1.set(xlabel='Giorni', ylabel='Ospedalizzati 15gg precedenti', title='Toscana - Deceduti giornalieri rispetto ospedalizzati 15gg precedenti')
    ax2.set(xlabel='Giorni', ylabel='Deceduti', title='')
    ax1.legend(labels=['Ospedalizzati'])
    ax2.legend(labels=['Deceduti'])
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    ax1.grid()
    plt.savefig('/home/marco/covidGraphs/DecedutiGioVSOsped15gpast_TOSCANA.png')
    #plt.show()

##############################################################################################################
# PRATO - SITUAZIONE
##############################################################################################################
if pratoCasi == True:
    
    #1
    casPo=[]
    casPoLog=[]
    casiPOh24=[]

    casPt=[]
    casPtLog=[]
    casiPth24=[]

    casFi=[]
    casFiLog=[]
    casiFih24=[]

    casBg=[]
    casBgLog=[]
    casBgh24=[]

    casLc=[]
    casLcLog=[]
    casLch24=[]

    casPi=[]
    casPiLog=[]
    casPih24=[]

    casAr=[]
    casArLog=[]
    casArh24=[]

    casGr=[]
    casGrLog=[]
    casGrh24=[]

    casLi=[]
    casLiLog=[]
    casLIh24=[]

    casMc=[]
    casMcLog=[]
    casMch24=[]

    casSi=[]
    casSiLog=[]
    casSih24=[]

    def elabCasiPO(tempS,url):
        if ( int(tempS)<10 ):
            url += '0'
        data = urllib.request.urlopen(url+tempS + '.csv')
        myData = data.read()
        mystr = myData.decode("utf8")
        data.close()
        mySplit = mystr.splitlines()

        #2 
        poRowSplit = mySplit[111].split(',') #Prato
        ptRowSplit = mySplit[110].split(',') #Pistoia
        fiRowSplit = mySplit[104].split(',') #Firenze
        bgRowSplit = mySplit[49].split(',')  #Bergamo
        lcRowSplit = mySplit[107].split(',') #Lucca
        piRowSplit = mySplit[109].split(',') #Pisa
        arRowSplit = mySplit[103].split(',') #Arezzo
        grRowSplit = mySplit[105].split(',') #Grosseto
        liRowSplit = mySplit[106].split(',') #Livorno
        mcRowSplit = mySplit[108].split(',') #Massa Carrara
        siRowSplit = mySplit[112].split(',') #Siena

        #3        
        if poRowSplit[9] == '':
            casiPO = 0
        else:
            casiPO = int(poRowSplit[9])
        
        if ptRowSplit[9] == '':
            casiPT = 0
        else:
            casiPT = int(ptRowSplit[9])

        if fiRowSplit[9] == '':
            casiFI = 0
        else:
            casiFI = int(fiRowSplit[9])
        
        if bgRowSplit[9] == '':
            casiBG = 0
        else:
            casiBG = int(bgRowSplit[9])    

        if lcRowSplit[9] == '':
            casiLC = 0
        else:
            casiLC = int(lcRowSplit[9])    
        
        if piRowSplit[9] == '':
            casiPI = 0
        else:
            casiPI = int(piRowSplit[9])

        if piRowSplit[9] == '':
            casiPI = 0
        else:
            casiPI = int(piRowSplit[9])
        
        if arRowSplit[9] == '':
            casiAR = 0
        else:
            casiAR = int(arRowSplit[9])
        
        if grRowSplit[9] == '':
            casiGR = 0
        else:
            casiGR = int(grRowSplit[9])
        
        if liRowSplit[9] == '':
            casiLI = 0
        else:
            casiLI = int(liRowSplit[9])
        
        if mcRowSplit[9] == '':
            casiMC = 0
        else:
            casiMC = int(mcRowSplit[9])

        if siRowSplit[9] == '':
            Casi_per_tamponi_Toscana = 0
        else:
            casiSI = int(siRowSplit[9])

        return [casiPO,casiPT,casiFI,casiBG,casiLC,casiPI,casiAR,casiGR,casiLI,casiMC,casiSI]

    def calcCasiPO(day,casi,mese):
        #4
        global casiPoOLd
        global casiPtOLd
        global casiFIOLd
        global casiBgOLd
        global casiLcOLd
        global casiPiOLd
        global casiArOLd
        global casiGrOLd
        global casiLiOLd
        global casiMcOLd
        global casiSiOLd

        month = ""
        if mese == 3:
            month = "Marzo"
        elif mese == 4:
            month = "Aprile" 
        elif mese == 5:
            month = "Maggio" 
        elif mese == 6:
            month = "Giugno" 

        #5
        casPo.append (casi[0])
        casiPOh24.append (casi[0]-casiPoOLd)
        if casi[0] == 0:
            casPoLog.append( 0 )
        else:
            casPoLog.append( math.log10(int(casi[0])) )
        
        casPt.append (casi[1])
        casiPth24.append (casi[1]-casiPtOLd)
        if casi[1] == 0:
            casPtLog.append( 0 )
        else:
            casPtLog.append( math.log10(int(casi[1])) )
        
        casFi.append (casi[2])
        casiFih24.append (casi[2]-casiFIOLd)
        if casi[2] == 0:
            casFiLog.append( 0 )
        else:
            casFiLog.append( math.log10(int(casi[2])) )
        
        casBg.append(casi[3])
        casBgh24.append (casi[3]-casiBgOLd)
        if casi[3] == 0:
            casBgLog.append( 0 )
        else:
            casBgLog.append( math.log10(int(casi[3])) )
        
        casLc.append(casi[4])
        casLch24.append (casi[4]-casiLcOLd)
        if casi[4] == 0:
            casLcLog.append( 0 )
        else:
            casLcLog.append( math.log10(int(casi[4])) )
        
        casPi.append(casi[5])
        casPih24.append (casi[5]-casiPiOLd)
        if casi[5] == 0:
            casPiLog.append( 0 )
        else:
            casPiLog.append( math.log10(int(casi[5])) )
        
        casAr.append(casi[6])
        casArh24.append (casi[6]-casiArOLd)
        if casi[6] == 0:
            casArLog.append( 0 )
        else:
            casArLog.append( math.log10(int(casi[6])) )

        casGr.append(casi[7])
        casGrh24.append (casi[7]-casiGrOLd)
        if casi[7] == 0:
            casGrLog.append( 0 )
        else:
            casGrLog.append( math.log10(int(casi[7])) )
        
        casLi.append(casi[8])
        casLIh24.append (casi[8]-casiLiOLd)
        if casi[8] == 0:
            casLiLog.append( 0 )
        else:
            casLiLog.append( math.log10(int(casi[8])) )

        casMc.append(casi[9])
        casMch24.append (casi[9]-casiMcOLd)
        if casi[9] == 0:
            casMcLog.append( 0 )
        else:
            casMcLog.append( math.log10(int(casi[9])) )
        
        casSi.append(casi[10])
        casSih24.append (casi[10]-casiSiOLd)
        if casi[10] == 0:
            casSiLog.append( 0 )
        else:
            casSiLog.append( math.log10(int(casi[10])) )

        print (day + ' ' + month + ' : ', end = '')
        print (" - casi rilevati:" + str(casi) )
        
        #6
        casiPoOLd = casi[0]
        casiPtOLd = casi[1]
        casiFIOLd = casi[2]
        casiBgOLd = casi[3]
        casiLcOLd = casi[4]
        casiPiOLd = casi[5]
        casiArOLd = casi[6]
        casiGrOLd = casi[7]
        casiLiOLd = casi[8]
        casiMcOLd = casi[9]
        casiSiOLd = casi[10]

    print (f"{bcolors.WARNING}PRATO - CASI{bcolors.ENDC}" )

    #7
    casiPoOLd = 0
    casiPtOLd = 0
    casiFIOLd = 0
    casiBgOLd = 0
    casiLcOLd = 0
    casiPiOLd = 0
    casiArOLd = 0
    casiGrOLd = 0
    casiLiOLd = 0
    casiMcOLd = 0
    casiSiOLd = 0

    for d in dayM:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202003')
        calcCasiPO(str(d),dat,3)
        
    for d in dayA:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202004')
        calcCasiPO(str(d),dat,4)

    for d in dayMay:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202005')
        calcCasiPO(str(d),dat,5)
    
    for d in dayJun:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202006')
        calcCasiPO(str(d),dat,6)

    fig90, ax1 = plt.subplots()
    ax1.bar(date, casPo)
    ax1.plot(date, casPo, color="red")
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato - Casi')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/PratoCasi.png')
    
    fig95, ax1 = plt.subplots()
    ax1.bar(date, casiPOh24)
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato - Casi giornalieri')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/PratoCasi_h24.png')

    fig100, ax1 = plt.subplots()
    ax1.plot(date, casPoLog)
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato - Casi - Scala log')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/PratoCasi_LOG.png')
    
    #8
    casPoPOP = [n/254608 for n in casPo]
    casPtPOP = [n/291839 for n in casPt]
    casFiPOP = [n/1014423 for n in casFi]
    casBgPOP = [n/1109933 for n in casBg]
    casLcPOP = [n/390042 for n in casLc]
    casPiPOP = [n/421851 for n in casPi]
    casArPOP = [n/344374 for n in casAr]
    casGrPOP = [n/223045 for n in casGr]
    casLiPOP = [n/337334 for n in casLi]
    casMcPOP = [n/196580 for n in casMc]
    casSiPOP = [n/268341 for n in casSi]


    #9
    casPoLOG = [math.log10(n) for n in casPo]
    casPtLOG = [math.log10(n) for n in casPt]
    casFiLOG = [math.log10(n) for n in casFi]
    casBgLOG = [math.log10(n) for n in casBg]
    casLcLog = [math.log10(n) for n in casLc]
    casPiLog = [math.log10(n) for n in casPi]
    casArLog = [math.log10(n) for n in casAr]
    casGrLog = [math.log10(n) for n in casGr]
    casLiLog = [math.log10(n) for n in casLi]
    casMcLog = [math.log10(n) for n in casMc]
    casSiLog = [math.log10(n) for n in casSi]

    #10
    fig110, ax1 = plt.subplots()
    ax1.plot(date, casPoPOP, linewidth=3, color="red")
    ax1.plot(date, casPtPOP, color="green")
    ax1.plot(date, casFiPOP, color="blue")
    #ax1.plot(date, casBgPOP, color="black")
    ax1.plot(date, casLcPOP, color="orange")
    ax1.plot(date, casPiPOP, color="purple")
    ax1.plot(date, casArPOP, color="cyan")
    ax1.plot(date, casGrPOP, color="magenta")
    ax1.plot(date, casLiPOP, color="gray")
    ax1.plot(date, casMcPOP, color="olive")
    ax1.plot(date, casSiPOP, color="pink")
    ax1.legend(labels=['Prato','Pistoia','Firenze','Lucca','Pisa','Arezzo','Grosseto','Livorno','Massa Carrara','Siena'])
    #ax1.legend(labels=['Prato','Pistoia','Firenze','Bergamo','Lucca','Pisa','Arezzo','Grosseto','Livorno','Massa Carrara','Siena'])
    #ax1.legend(labels=['Prato'])
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato casi per popolazione')
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato VS altre provincie, casi per popolazione')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/PratoVSPistiaVSFIrenze_casi_per_popolazione.png')

    '''
    #11
    yticks = [0, 10, 32, 100, 316, 1000, 3162]
    fig115, ax1 = plt.subplots()
    ax1.plot(date, casPoLOG, linewidth=3, color="red")
    
    ax1.plot(date, casPtLOG, color="green")
    ax1.plot(date, casFiLOG, color="blue")
    #ax1.plot(date, casBgLOG, color="black")
    ax1.plot(date, casLcLog, color="orange")
    ax1.plot(date, casPiLog, color="purple")
    ax1.plot(date, casArLog, color="cyan")
    ax1.plot(date, casGrLog, color="magenta")
    ax1.plot(date, casLiLog, color="gray")
    ax1.plot(date, casMcLog, color="olive")
    ax1.plot(date, casSiLog, color="pink")
    
    #ax1.legend(labels=['Prato','Pistoia','Firenze','Lucca','Pisa','Arezzo','Grosseto','Livorno','Massa Carrara','Siena'])
    ax1.legend(labels=['Prato'])
    #ax1.legend(labels=['Prato','Pistoia','Firenze','Bergamo','Lucca','Pisa','Arezzo','Grosseto','Livorno','Massa Carrara','Siena'])
    #ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato casi per popolazione logaritmica')
    ax1.set(xlabel='Giorni', ylabel='Casi', title='Prato VS altre provincie, casi per popolazione logaritmica')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.set_yticklabels(["$%.1f$" % y for y in yticks])
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/PratoVSPistiaVSFIrenze_casi_per_popolazione_LOG.png')

    '''

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
    #plt.show()
    
    fig120, ax1 = plt.subplots()
    ax1.plot(date, casiTampArItLog)
    ax1.plot(date, casiTampArTOLog)
    ax1.set(xlabel='Giorni', ylabel='Casi',
        title='Casi per tamponi - Confronto andamento Nazionale/Toscana (scala log)')
    ax1.grid()
    #plt.show()

##############################################################################################################
# MERGING PICTURES
##############################################################################################################

#Italia vs Toscana casi/tamponi
im1 = Image.open('/home/marco/covidGraphs/Casi_per_tamponi_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Casi_per_tamponi_Toscana.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Casi_per_tamponi_ItaliaVSToscana.png')

#Italia vs Toscana ospedalizzati (barre)
im1 = Image.open('/home/marco/covidGraphs/Totale_Ospedalizzati_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Totale_Ospedalizzati_Toscana.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Totale_Ospedalizzati_ItaliaVSToscana.png')

#Italia vs Toscana Deceduti/Dimessi/Ospedalizzati
im1 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Dec_Dim_Osp_ItaliaVSToscana.png')

#Italia vs Toscana Deceduti/Dimessi/Ospedalizzati VARH24
im1 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Italia_VARH24.png')
im2 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana_VARH24.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Dec_Dim_Osp_ItaliaVSToscana_VARH24.png')

#Italia vs Toscana Deceduti/Dimessi/Ospedalizzati VARH24
im1 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Italia_LOG.png')
im2 = Image.open('/home/marco/covidGraphs/Dec_Dim_Osp_Toscana_LOG.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Dec_Dim_Osp_ItaliaVSToscana_LOG.png')

#Italia vs Toscana Deceduti/Dimessi/Ospedalizzati VARH24
im1 = Image.open('/home/marco/covidGraphs/Terapie_Intensive_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Terapie_Intensive_Toscana.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Ter_Int_ItaliaVSToscana.png')

#Italia vs Toscana Deceduti/Dimessi/Ospedalizzati VARH24
im1 = Image.open('/home/marco/covidGraphs/DecedutiGioVSOsped15gpast_ITA.png')
im2 = Image.open('/home/marco/covidGraphs/DecedutiGioVSOsped15gpast_TOSCANA.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/DecedutiGioVSOsped15gpast.png')

#Italia vs Toscana Deceduti VARH24
im1 = Image.open('/home/marco/covidGraphs/Decessi_24h_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Decessi_24h_Toscana.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Deceduti24h_ITA_vs_TOSCANA.png')

#Prato casi tot e h24
im1 = Image.open('/home/marco/covidGraphs/PratoCasi.png')
im2 = Image.open('/home/marco/covidGraphs/PratoCasi_h24.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/Prato_situazione.png')

'''
#Prato casi tot e h24
im1 = Image.open('/home/marco/covidGraphs/PratoVSPistiaVSFIrenze_casi_per_popolazione.png')
im2 = Image.open('/home/marco/covidGraphs/PratoVSPistiaVSFIrenze_casi_per_popolazione_LOG.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.save('/home/marco/covidGraphs/output/PratoVSPistiaVSFIrenze_casi_per_popolazione.png')
'''