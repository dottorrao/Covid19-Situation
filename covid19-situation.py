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
color.write ("ITALIA - POSITIVI PER TAMPONI EFFETTUATI \n","STRING")
dayM = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30] #marzo
dayA = [] #aprile
date=[]
casi=0
tamponi=0
##############################################################################################################

casiTampArIt=[]
casiArIt=[]
for d in dayM:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003' + tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mystrSPLIT = mystr.split(",")
    casi = int(mystrSPLIT[25])
    tamponi = int(mystrSPLIT[26])
    print (tempS + ' Marzo:', end = '')
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiTampArIt.append (ct)
    casiArIt.append( math.log10(int(casi)) )
    date.append(datetime(year=2020, month=3, day=d))
    print (str(ct), end = '')
    print (" - casi rilevati:" + str(casi), end = '')
    print (" - tamponi effettuati:" + str(tamponi) )

for d in dayA:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202004' + tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mystrSPLIT = mystr.split(",")
    casi = int(mystrSPLIT[25])
    tamponi = int(mystrSPLIT[26])
    print (tempS + ' Aprile:', end = '')
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiArIt.append( math.log10(int(casi)) )
    casiTampArIt.append (ct)
    date.append(datetime(year=2020, month=4, day=d))
    print (str(ct), end = '')
    print (" - casi rilevati:" + str(casi), end = '')
    print (" - tamponi effettuati:" + str(tamponi) )

plt.plot(date,casiTampArIt)
plt.ylabel('Casi per tamponi')
plt.xlabel('Giorni')
plt.title ( 'Italia - Casi per tamponi')
plt.show()

plt.plot(date,casiArIt)
plt.ylabel('Casi')
plt.xlabel('Giorni')
plt.title ( 'Italia - Casi scala log')
plt.show()

##############################################################################################################
color.write ("ITALIA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )
terapianInOLd = 0
terInIt=[]
for d in dayM:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003' + tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mystrSPLIT = mystr.split(",")
    terapianIn = int(mystrSPLIT[17])
    terInIt.append (terapianIn)
    diff = ( terapianIn - terapianInOLd )
    print (tempS + ' Marzo:' + str(terapianIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terapianInOLd = terapianIn

for d in dayA:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale-202003' + tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mystrSPLIT = mystr.split(",")
    terapianIn = int(mystrSPLIT[17])
    terInIt.append (terapianIn)
    diff = ( terapianIn - terapianInOLd )
    print (tempS + ' Aprile:' + str(terapianIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terapianInOLd = terapianIn

plt.plot(date,terInIt)
plt.ylabel('Terapie Intensive')
plt.xlabel('Giorni')
plt.title ('Italia - Ricoveri terapia intensiva')
plt.show()

##############################################################################################################
color.write ("TOSCANA- POSITIVI PER TAMPONI EFFETTUATI \n","STRING" )
casiArTampTo=[]
casiArTo=[]
for d in dayM:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003'+ tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mySplit = mystr.splitlines()
    regionSplit = mySplit[17].split(",")
    casi = int(regionSplit[15])
    tamponi = int(regionSplit[16])
    print (tempS + ' Marzo:', end = '')
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiArTampTo.append (ct)
    casiArTo.append( math.log10(int(casi)) )
    print ( format(round(casi/tamponi,5),'.5f'), end = '')
    print (" - casi rilevati: " + str(casi), end = '')
    print (" - tamponi effettuati: " + str(tamponi) )

for d in dayA:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003'+ tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mySplit = mystr.splitlines()
    regionSplit = mySplit[17].split(",")
    casi = int(regionSplit[15])
    tamponi = int(regionSplit[16])
    print (tempS + ' Aprile:', end = '')
    ct = float( (format(round(casi/tamponi,5),'.5f')) )
    casiArTampTo.append (ct)
    casiArTo.append( math.log10(int(casi)) )
    print ( format(round(casi/tamponi,5),'.5f'), end = '')
    print (" - casi rilevati: " + str(casi), end = '')
    print (" - tamponi effettuati: " + str(tamponi) )

plt.plot(date,casiArTampTo)
plt.title ('Toscana - Casi per tamponi')
plt.xlabel('Giorni')
plt.ylabel('Casi')
plt.show()

plt.plot(date,casiArTo)
plt.title ('Toscana - Casi scala log')
plt.xlabel('Giorni')
plt.ylabel('Casi')
plt.show()

##############################################################################################################
color.write ("TOSCANA - INCREMENTO RICOVERATI TERAPIA INTENSIVA \n","STRING" )
day = [10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
terapianInOLd = 0
terInTo=[]
for d in dayM:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003'+ tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mySplit = mystr.splitlines()
    regionSplit = mySplit[17].split(",")
    terapianIn = int ( regionSplit[7] )
    terInTo.append (terapianIn)
    diff = ( terapianIn - terapianInOLd )
    print (tempS + ' Marzo: ' + str(terapianIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terapianInOLd = terapianIn

for d in dayA:
    tempS = str(d)
    data = urllib.request.urlopen('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-202003'+ tempS + '.csv')
    myData = data.read()
    mystr = myData.decode("utf8")
    data.close()
    mySplit = mystr.splitlines()
    regionSplit = mySplit[17].split(",")
    terapianIn = int ( regionSplit[7] )
    terInTo.append (terapianIn)
    diff = ( terapianIn - terapianInOLd )
    print (tempS + ' Aprile: ' + str(terapianIn), end = '')
    print (" - Differenza giorno prec: " + str(diff) )
    terapianInOLd = terapianIn

plt.plot(date, terInTo)
plt.ylabel('Casi per tamponi')
plt.xlabel('Giorni')
plt.title ('Toscana - Ricoveri terapia intensiva')
plt.show()
