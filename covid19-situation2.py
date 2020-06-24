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
dayMar = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #marzo
dayApr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] #aprile
dayMay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #maggio
dayJun = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]#Giugno
date=[]
casi=0
tamponi=0
regione = ""

## FLAG PROCESSING VARIE SEZIONI
italiaCasiTampone = True
toscanaCasiTampone = True
lombardiaCasiTampone = True
dettaglioToscana =  True

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
    '''
    for d in dayMar:
        date.append(datetime(year=2020, month=3, day=d, hour = 18, minute = 30, second = 0))
    for d in dayApr:
        date.append(datetime(year=2020, month=4, day=d, hour = 18, minute = 30, second = 0))
    '''
    for d in dayMay:
        date.append(datetime(year=2020, month=5, day=d, hour = 18, minute = 30, second = 0))
    for d in dayJun:
        date.append(datetime(year=2020, month=6, day=d, hour = 18, minute = 30, second = 0))

##############################################################################################################

makeCalendar()

##############################################################################################################
# ITALIA - CASI PER TAMPONI - DECEDUTI - Media ultimi 7 Giorni
##############################################################################################################
if italiaCasiTampone == True:
    
    casiTampArIt=[]
    casiTampArIth24=[]
    casiTampArItLog=[]
    casiTampArIth24M7gg=[0,0,0,0,0,0,0]
    decedutiIth24M7gg=[0,0,0,0,0,0,0]
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
        if ( cth24 > 0 ):
            casiTampArIth24Log.append ( math.log10(cth24) )
        else:
            casiTampArIth24Log.append ( 0 )
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
        
    print (f"{bcolors.WARNING}ITALIA - POSITIVI PER TAMPONI / DECESSI GIORNALIERI (Media ultimi 7 giorni) {bcolors.ENDC}")

    #variabili per salvataggio valori giorno precedente
    casiTampOld = [205463,1979217]  #inizializzo ai dati del 9 marzo
    casiOld = 205463                #inizializzo ai dati del 9 marzo
    decedutiOld = 27967             #da inizializzare ai dati del 9 marzo
    
    '''
    for d in dayMar:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
        calcCasiTampone(str(d),dat,3)
    '''

    '''
    for d in dayApr:
        dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
        calcCasiTampone(str(d),dat,4)
    '''

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

    #10 - casi per tampone media ultimi 7 giorni
    l=len (casiTampArIth24)
    for i in range (7,l):
        casiTampArIth24M7gg.append(sum(casiTampArIth24[i-6:i+1])/7)
    
    l=len (casiTampArIth24M7gg)
    print ("Italia - Media casi/tamponi ultimi 7 giorni: " + str(casiTampArIth24M7gg[l-1]) + " ** Ieri: " + str(str(casiTampArIth24M7gg[l-2])) ) 
    print (casiTampArIth24M7gg)

    #Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h media 7GG
    fig10, ax1 = plt.subplots()
    ax1.bar(date, casiTampArIth24M7gg)
    ax1.legend(labels=['Casi per tampone'])
    ax1.set(xlabel='Giorni', ylabel='Casi per tampone', title='Italia - Casi per tampone - Media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/italia_casi_per_tampone_media7gg.png') 

    #11 - Deceduti Italia - Media ultimi 7gg
    l=len (decedutiIth24)
    for i in range (7,l):
        decedutiIth24M7gg.append(sum(decedutiIth24[i-6:i+1])/7)
    
    l=len (decedutiIth24M7gg)
    print ("Italia - Media deceduti ultimi 7 giorni: " + str(decedutiIth24M7gg[l-1]) + " ** Ieri: " + str (decedutiIth24M7gg[l-2]) ) 

    #Deceduti Italia - Media ultimi 7gg
    fig10, ax1 = plt.subplots()
    ax1.bar(date, decedutiIth24M7gg)
    ax1.legend(labels=['Deceduti'])
    ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Italia - Deceduti - media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/italia_deceduti_media7gg.png') 

##############################################################################################################
# TOSCANA - POSITIVI PER TAMPONI
##############################################################################################################
if toscanaCasiTampone == True:

    casiTampArTO=[]
    casiTampArTOh24=[]
    casiTampArTOLog=[]
    tamponih24TO=[]
    casiTampArTOh24M7gg=[0,0,0,0,0,0,0]
    decedutiTOh24M7gg=[0,0,0,0,0,0,0]
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

    casiTampOldTO = [9352,141849]  #inizializzo ai dati del 9 marzo per la toscana
    casiOldTO = 9352               #da inizializzare
    decessiOld = 842               #da inizializzare

    '''
    for d in dayMar:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTampArTO(str(d),dat,3)

    for d in dayApr:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTampArTO(str(d),dat,4)
    '''

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

    #10 - casi per tampone media ultimi 7 giorni
    l=len (casiTampArTOh24)
    for i in range (7,l):
        casiTampArTOh24M7gg.append(sum(casiTampArTOh24[i-6:i+1])/7)
    
    l=len (casiTampArTOh24M7gg)
    print ("Toscana - Media casi/tamponi ultimi 7 giorni: " + str(casiTampArTOh24M7gg[l-1]) + " ** Ieri: " + str(str(casiTampArTOh24M7gg[l-2])) ) 
        
    #Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h media 7GG
    fig10, ax1 = plt.subplots()
    ax1.bar(date, casiTampArTOh24M7gg)
    ax1.legend(labels=['Casi per tampone'])
    ax1.set(xlabel='Giorni', ylabel='Casi per tampone', title='Toscana - Casi per tampone - Media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/toscana_casi_per_tamponi_media7gg.png') 

    #11 - Deceduti Toscana - Media ultimi 7gg
    l=len (dech24TO)
    for i in range (7,l):
        decedutiTOh24M7gg.append(sum(dech24TO[i-6:i+1])/7)
    
    l=len (decedutiTOh24M7gg)
    print ("Toscana - Media deceduti ultimi 7 giorni: " + str(decedutiTOh24M7gg[l-1]) + " ** Ieri: " + str(str(decedutiTOh24M7gg[l-2])) ) 

    #Deceduti Toscana - Media ultimi 7gg
    fig10, ax1 = plt.subplots()
    ax1.bar(date, decedutiTOh24M7gg)
    ax1.legend(labels=['Deceduti'])
    ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Toscana - Deceduti - media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/toscana_deceduti_media7gg.png') 

##############################################################################################################
# LOMBARDIA - POSITIVI PER TAMPONI
##############################################################################################################
if lombardiaCasiTampone == True:

    casiTampArTO=[]
    casiTampArTOh24=[]
    casiTampArTOLog=[]
    tamponih24TO=[]
    casiTampArTOh24M7gg=[0,0,0,0,0,0,0]
    decedutiTOh24M7gg=[0,0,0,0,0,0,0]
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
        regionSplit = mySplit[10].split(",") #lombardia
        #regionSplit = mySplit[17].split(",") #toscana
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

    print (f"{bcolors.WARNING}LOMBARDIA - POSITIVI PER TAMPONI / DECESSI GIORNALIERI{bcolors.ENDC}" )

    casiTampOldTO = [75732,376943]  
    casiOldTO = 75732               
    decessiOld = 13772              

    '''
    for d in dayMar:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
        calcCasiTampArTO(str(d),dat,3)

    for d in dayApr:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
        calcCasiTampArTO(str(d),dat,4)
     '''

    for d in dayMay:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202005')
        calcCasiTampArTO(str(d),dat,5)
    
    for d in dayJun:
        dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202006')
        calcCasiTampArTO(str(d),dat,6)

    #1 - Casi per tampone Lombardia
    fig60, ax1 = plt.subplots()
    ax1.bar(date, tamponih24TO)
    ax1.legend(labels=['Tamponi giornalieri'])
    ax2 = ax1.twinx()
    ax2.plot(date, casiTampArTOh24,color='tab:orange',linewidth=3)
    ax2.plot(date, casiTampArTO,color='tab:red',linewidth=3)
    ax2.legend(labels=['Casi/Tamponi h24', 'Casi/Tamponi da inizio'])
    ax1.set(xlabel='Giorni', ylabel='Tamponi Giornalieri',
        title='Casi per tamponi Lombardia - Confronto andamento inizio epidemia/giornaliero')
    ax2.set(xlabel='Giorni', ylabel='Casi per tampone',
        title='Casi per tamponi Lombardia - Confronto andamento inizio epidemia/giornaliero')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/Casi_per_tamponi_Lombardia.png') 
    ##plt.show()

    #10 - casi per tampone media ultimi 7 giorni
    l=len (casiTampArTOh24)
    for i in range (7,l):
        casiTampArTOh24M7gg.append(sum(casiTampArTOh24[i-6:i+1])/7)
    
    l=len (casiTampArTOh24M7gg)
    print ("Lombardia - Media casi/tamponi ultimi 7 giorni: " + str(casiTampArTOh24M7gg[l-1]) + " ** Ieri: " + str(str(casiTampArTOh24M7gg[l-2])) )
    print ( casiTampArTOh24M7gg )
        
    #Casi per tamponi Italia - Confronto andamento inizio epidemia/giornaliero ultime 24h media 7GG
    fig10, ax1 = plt.subplots()
    ax1.bar(date, casiTampArTOh24M7gg)
    ax1.legend(labels=['Casi per tampone'])
    ax1.set(xlabel='Giorni', ylabel='Casi per tampone', title='Lombardia - Casi per tampone - Media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/lombardia_casi_per_tamponi_media7gg.png') 

    #11 - Deceduti Lombardia - Media ultimi 7gg
    l=len (dech24TO)
    for i in range (7,l):
        decedutiTOh24M7gg.append(sum(dech24TO[i-6:i+1])/7)
    
    l=len (decedutiTOh24M7gg)
    print ("Lombardia - Media deceduti ultimi 7 giorni: " + str(decedutiTOh24M7gg[l-1]) + " ** Ieri: " + str(str(decedutiTOh24M7gg[l-2])) )

    #Deceduti Lombardia - Media ultimi 7gg
    fig10, ax1 = plt.subplots()
    ax1.bar(date, decedutiTOh24M7gg)
    ax1.legend(labels=['Deceduti'])
    ax1.set(xlabel='Giorni', ylabel='Deceduti', title='Lombardia - Deceduti - media a 7gg')
    ax1.grid()
    ax1.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))  
    ax1.xaxis.set_tick_params(rotation=90)
    plt.savefig('/home/marco/covidGraphs/lombardia_deceduti_media7gg.png') 

##############################################################################################################
# PRATO - SITUAZIONE
##############################################################################################################
if dettaglioToscana ==  True:

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
    casiPoOLd = 520
    casiPtOLd = 630
    casiFIOLd = 3120
    casiBgOLd = 11313
    casiLcOLd = 1276
    casiPiOLd = 847
    casiArOLd = 624
    casiGrOLd = 406
    casiLiOLd = 513
    casiMcOLd = 994
    casiSiOLd = 422
    
    '''
    for d in dayMar:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202003')
        calcCasiPO(str(d),dat,3)
        
    for d in dayApr:
        dat = elabCasiPO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province-202004')
        calcCasiPO(str(d),dat,4)
    '''

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

##############################################################################################################
# MERGING PICTURES
##############################################################################################################

#Italia vs Toscana&Lombardia casi/tamponi
im1 = Image.open('/home/marco/covidGraphs/Casi_per_tamponi_Italia.png')
im2 = Image.open('/home/marco/covidGraphs/Casi_per_tamponi_Toscana.png')
im3 = Image.open('/home/marco/covidGraphs/Casi_per_tamponi_Lombardia.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height + im3.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.paste(im3, (0, 2*(im2.height)))
dst.save('/home/marco/covidGraphs/output2_0/Casi_per_tamponi_ItaliaVSToscana_Lombardia.png')

#Italia vs Toscana&Lombardia casi/tamponi media 7gg
im1 = Image.open('/home/marco/covidGraphs/italia_casi_per_tampone_media7gg.png')
im2 = Image.open('/home/marco/covidGraphs/toscana_casi_per_tamponi_media7gg.png')
im3 = Image.open('/home/marco/covidGraphs/lombardia_casi_per_tamponi_media7gg.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height + im3.height))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.paste(im3, (0, 2*(im2.height)))
dst.save('/home/marco/covidGraphs/output2_0/italia_vs_toscana&lombardia_casi_per_tampone_media7gg.png')

#Italia vs Toscana&Lombardia deceduti media 7gg
im1 = Image.open('/home/marco/covidGraphs/italia_deceduti_media7gg.png')
im2 = Image.open('/home/marco/covidGraphs/toscana_deceduti_media7gg.png')
im3 = Image.open('/home/marco/covidGraphs/lombardia_deceduti_media7gg.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height + im2.height ))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.paste(im3, (0, 2*(im2.height)))
dst.save('/home/marco/covidGraphs/output2_0/italia_vs_toscana&lombardia_deceduti_media7gg.png')

#Prato situazione
im1 = Image.open('/home/marco/covidGraphs/PratoCasi_h24.png')
im2 = Image.open('/home/marco/covidGraphs/PratoCasi.png')
im3 = Image.open('/home/marco/covidGraphs/PratoVSPistiaVSFIrenze_casi_per_popolazione.png')
dst = Image.new('RGB', (im1.width, im1.height + im2.height + im2.height ))
dst.paste(im1, (0, 0))
dst.paste(im2, (0, im1.height))
dst.paste(im3, (0, 2*(im2.height)))
dst.save('/home/marco/covidGraphs/output2_0/prato_situazione.png')