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
import numpy as np
import math
from datetime import datetime, timedelta
try: color = sys.stdout.shell
except AttributeError: raise RuntimeError("Use IDLE")

##############################################################################################################
#GLOBAL VARS
dayM = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31] #marzo
dayA = [1,2] #aprile
date=[]
casi=0
tamponi=0
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
##############################################################################################################


##############################################################################################################
# ITALIA - CASI PER TAMPONI
##############################################################################################################
casiTampArIt=[]
casiTampArItLog=[]

def elabCasiTampArIt(tempS,url):
    data = urllib.request.urlopen(url+tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mystrSPLIT = mystr.split(",")
    casi = int(mystrSPLIT[25])
    tamponi = int(mystrSPLIT[26])
    dat = [casi,tamponi]  
    return dat

def calcCasiTampone(day,casi,tamponi,mese):
    month = ""
    if mese == 3:
        month = "Marzo"
    elif mese == 4:
        month = "Arile" 
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiTampArIt.append (ct)
    casiTampArItLog.append( math.log10(int(dat[0])) )
    date.append(datetime(year=2020, month=mese, day=d))
    print (day + ' ' + month + ' : ', end = '')
    print (str(ct), end = '')
    print (" - casi rilevati:" + str(dat[0]), end = '')
    print (" - tamponi effettuati:" + str(dat[1]) )

color.write ("ITALIA - POSITIVI PER TAMPONI EFFETTUATI \n","STRING")

for d in dayM:
    dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
    calcCasiTampone(str(d),dat[0],dat[1],3)
    
for d in dayA:
    dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-2020040')
    calcCasiTampone(str(d),dat[0],dat[1],4)

plotGraph(date,casiTampArIt,'Giorni','Casi per tamponi','Italia - Casi per tamponi')
plotGraph(date,casiTampArItLog,'Giorni','Casi per tamponi','Italia - Casi per tamponi (scala log.)')

##############################################################################################################
#ITALIA - TERAPIA INTENSIVA
##############################################################################################################

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

color.write ("ITALIA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )
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
color.write ("TOSCANA- POSITIVI PER TAMPONI EFFETTUATI \n","STRING" )
casiTampArTo=[]
casiTampArToLog=[]

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
    month = ""
    if mese == 3:
        month = "Marzo"
    elif mese == 4:
        month = "Arile"
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiTampArTo.append (ct)
    casiTampArToLog.append( math.log10(int(casi)) )
    print (day + ' ' + month + ' : ', end = '')
    print (str(ct), end = '')
    print (" - casi rilevati: " + str(casi), end = '')
    print (" - tamponi effettuati: " + str(tamponi) )
    
for d in dayM:
    dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
    calcCasiTampArTO(str(d),dat[0],dat[1],3)

for d in dayA:
    dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-2020040')
    calcCasiTampArTO(str(d),dat[0],dat[1],3)
   
plotGraph(date,casiTampArTo,'Giorni','Casi per tamponi','Toscana - Casi per tamponi')
plotGraph(date,casiTampArToLog,'Giorni','Casi per tamponi','Toscana - Casi per tamponi (scala log.)')


##############################################################################################################
# TOSCANA - TERAPIA INTENSIVA
##############################################################################################################

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
    
color.write ("TOSCANA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )

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
        month = "Arile" 

    casPo.append (casi)

    if casi == 0:
        casPoLog.append( 0 )
    else:
        casPoLog.append( math.log10(int(casi)) )
    
    print (day + ' ' + month + ' : ', end = '')
    print (" - casi rilevati:" + str(casi) )

color.write ("PRATO - CASI \n","STRING")

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
plt.plot(date,casiTampArIt)
plt.plot(date,casiTampArTo)
plt.ylabel("Casi")
plt.xlabel("Giorni")
plt.title ("Casi per tamponi - Confronto andamento Nazionale/Toscana")
plt.show()

plt.plot(date,casiTampArItLog)
plt.plot(date,casiTampArToLog)
plt.ylabel("Casi")
plt.xlabel("Giorni")
plt.title ("Casi per tamponi - Confronto andamento Nazionale/Toscana (scala log)")
plt.show() 

