#!/usr/bin/python3
# -*- coding: utf-8 -*-

import Adafruit_DHT
import Adafruit_BMP.BMP085
import sys, time

myGPIOPIN = 23	#Pin an dem DHT angeschaltet ist

#Auswahl Sensor
#mySensor = Adafruit_DHT.DHT11
mySensor = Adafruit_DHT.DHT22
#mySensor = Adafruit_DHT.AM2302

#Nur fuer DHT --> Wiederholungen nicht zu hoch waehlen: Achtung bei 10 und 15 sind das 10x15x2 Sekunden = 300 Sekunden!!!!
myRetries = 3      #Anzahl der Versuche zum Start des Lesens wenn Werte bekommen, diese jedoch nicht plausibel
myReadRetries = 6  #Anzahl der Versuche zum Lesen der Daten vom DHT (zwischen Lesen 2 Sekunde Pause)

#optionales Log zum Testen - ABER nur fuer DHT
#nur bei Bedarf auf True setzen --> Datei wird immer groesser!!!
#myLog = True
myLog = False
myLogFile = '/etc/openhab2/scripts/weather.log'

def logging(locReason, locHumidity, locTemperature):
    if (myLog):
        myFile = open(myLogFile,'a')
        myFile.write(time.strftime('%d.%m.%Y  %H:%M:%S') + ' Argument: ' + locReason +' - Luftfeuchtigkeit: '+ str(locHumidity) +'  - Temperatur: ' + str(locTemperature) + 'r')
        myFile.close()

def info():
    print ('Bitte Uebergabe von temperature, humidity, pressure, sealevel_pressure, altitude oder temperature2')
    print ('DHT-Sensor:')
    print ('temperature = Temperatur')
    print ('humidity = Luftfeuchtigkeit')
    print ('BMP-Sensor:')
    print ('pressure = Luftdruck')
    print ('sealevel_pressure = Luftdruck auf Meereshoehe')
    print ('altitude = Hoehe')
    print ('temperature2 = Temperatur')
    
if len(sys.argv) > 1:
    myArgument = sys.argv[1].lower()
    if (myArgument == 'temperature') or (myArgument == 'humidity'):
        for i in range(myRetries):
            myHumidity, myTemperature = Adafruit_DHT.read_retry(mySensor, myGPIOPIN, myReadRetries)
            #myHumidity, myTemperature = Adafruit_DHT.read(mySensor, myGPIOPIN)
            if (myHumidity is None or myTemperature is None):
                logging ('KEINE WERTE BEKOMMEN', myHumidity, myTemperature)
                quit()  #keine Werte (auch keine falschen) bekommen
            else:
                #falsche Werte anhand gueltiger Luftfeuchtigkeit (0-100) und Temperatur (-50 - 50) bestimmen
                if (myHumidity>0 and myHumidity-50 and myTemperature <50):
                    logging (myArgument, myHumidity, myTemperature)
                    if (myArgument == 'temperature'):
                        print (myTemperature)
                        quit()
                    elif (myArgument == 'humidity'):
                        print (myHumidity)
                        quit()
            time.sleep (2)
        logging ('WERTE NICHT GUELTIG', myHumidity, myTemperature)

    elif (myArgument == 'pressure'):
        myBMP = Adafruit_BMP.BMP085.BMP085()
        print(myBMP.read_pressure() / 100.0) #Ausgabe in  hPa (gebraeuchliche Art)
        #print(myBMP.read_pressure() / 1000.00) #Ausgabe in  kPa (bessere Skalierung im grid)
    elif (myArgument == 'sealevel_pressure'):
        myBMP = Adafruit_BMP.BMP085.BMP085()
        print(myBMP.read_sealevel_pressure() / 100.0) #Ausgabe in  hPa (gebraeuchliche Art)
        #print(myBMP.read_sealevel_pressure() / 1000.00) #Ausgabe in  kPa (bessere Skalierung im grid)
    elif (myArgument == 'altitude'):
        myBMP = Adafruit_BMP.BMP085.BMP085()
        print(myBMP.read_altitude())
    elif (myArgument == 'temperature2'):
        myBMP = Adafruit_BMP.BMP085.BMP085()
        print(myBMP.read_temperature())
    else:
        info()
else:
    info()
