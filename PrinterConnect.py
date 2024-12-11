import serial
from datetime import date, time, datetime

#Setting up com port settings


def Printer(PrinterPort,PrintInfo, Data):

    PrintConnecT= serial.Serial(port=PrinterPort,baudrate=9600,timeout=1)

    Check=PrintConnecT.is_open

    #Check coneection

    if Check:
        ScaleFormat=Data
        if PrintInfo==True:
            PrintConnecT.write(ScaleFormat)

    PrintConnecT.close    








    

