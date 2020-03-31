##############################################################################################################
#develop
##############################################################################################################

#IMPORT SECTION
import urllib.request
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
dayM = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] #marzo
dayA = [] #aprile
date=[]
casi=0
tamponi=0
##############################################################################################################


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
casiArIt=[]

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
    casiArIt.append( math.log10(int(dat[0])) )
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
    dat = elabCasiTampArIt(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004')
    calcCasiTampone(str(d),dat[0],dat[1],4)

plotGraph(date,casiTampArIt,'Giorni','Casi per tamponi','Italia - Casi per tamponi')
plotGraph(date,casiArIt,'Giorni','Casi','Italia - Casi scala log')

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
    terInIt.append (terIn)
    diff = ( terIn - terInOLd )
    print (day + ' ' + month + ' : ' + str(terIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terInOLd = terIn

color.write ("ITALIA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )
terInOLd = 0
terInIt=[]
for d in dayM:
    dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003')
    calcCasiTerInITA(str(d),dat,3)
    
for d in dayA:
    dat = elabCasiTerInITA(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004s')
    calcCasiTerInITA(str(d),dat,4)
    
plotGraph(date,terInIt,'Giorni','Terapie Intensive','Italia - Ricoveri terapia intensiva')


##############################################################################################################
# TOSCANA - CASI PER TAMPONI
##############################################################################################################
color.write ("TOSCANA- POSITIVI PER TAMPONI EFFETTUATI \n","STRING" )
casiArTampTo=[]
casiArTo=[]

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
    casiArTampTo.append (ct)
    casiArTo.append( math.log10(int(casi)) )
    print (day + ' ' + month + ' : ', end = '')
    print (str(ct), end = '')
    print (" - casi rilevati: " + str(casi), end = '')
    print (" - tamponi effettuati: " + str(tamponi) )
    
for d in dayM:
    dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
    calcCasiTampArTO(str(d),dat[0],dat[1],3)

for d in dayA:
    dat = elabCasiTampArTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
    calcCasiTampArTO(str(d),dat[0],dat[1],3)
   
plotGraph(date,casiArTampTo,'Giorni','Casi per tamponi','Toscana - Casi per tamponi')
plotGraph(date,casiArTo,'Giorni','Casi','Toscana - Casi scala log')


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
    diff = ( terIn - terInOLd )
    print (day + ' ' + month + ' : ' + str(terIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terInOLd = terIn
    
color.write ("TOSCANA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )

terInOLd = 0
terInTo=[]
for d in dayM:
    dat = elabCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003')
    calcCasiTerInTO(str(d),dat,3)

for d in dayA:
    dat = calcCasiTerInTO(str(d),'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202004')
    calcCasiTerInTO(str(d),dat,4)

plotGraph(date,terInTo,'Giorni','Terapie Intensive','Italia - Ricoveri terapia intensiva')
