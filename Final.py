import serial
from datetime import datetime
import SQL
import  PrinterConnect
import logging

# Setting up info logger.
LoggerInfo=logging.getLogger('DATA INFO LOGGER')
handler=logging.FileHandler('InfoFile.log')
format=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setLevel(logging.INFO)
handler.setFormatter(format)
LoggerInfo.addHandler(handler)

#Setting up error logger
LoggerError=logging.getLogger('ERROR LOGGER')
handler1=logging.FileHandler('ErrorFile.log')
format1=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler1.setLevel(logging.ERROR)
handler1.setFormatter(format1)
LoggerInfo.addHandler(handler1)
#Setting scale port parameters

def Auto(ScalePort,PrinterPort,id):
    ConnectScale= serial.Serial(port=ScalePort,baudrate=9600,timeout=2)
    if id==1 and ConnectScale.is_open:
        
        print("Connection established")
        #Check to see if the COM6 port is open, if true then code the while loop will run
        while ConnectScale.is_open:

            SerialData=ConnectScale.read(120)
           
            if len(SerialData)>5:
                InputD=SerialData.decode().splitlines()
                print(InputD)
                dataSize=len(SerialData)
                LoggerInfo.info("Streaming Data Size:%s",SerialData)

                #error handling for list indexes should be hear, print something
                if len(InputD)<6:
                    Mode='No mode'
                    LoggerError.error("%s: Data length not reach, missing data",InputD)
                    Message='Error with Passed data, please try again'
                    Format=Message.encode()
                    SetPrinterIn=PrinterConnect.Printer(PrinterPort,True,Format)
                    return Mode
                
                #WeighIn Mode
                if dataSize >1 and dataSize <90:
                    #set weigh in mode 
                    printerDataIn=SerialData
                    Gross=""
                    Mode="WEIGH IN"
                    print("Weigh In")
                    for item in range(len(InputD)+1):
                        match item:
                            case 1:
                                TruckId=InputD[item][11:]

                            case 3:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    search=word.isnumeric()

                                    if search:
                                        Gross+=word

                            case 5:
                                try:
                                    Date=datetime.strptime(InputD[item][8:],"%m/%d/%Y")
                                    Time=datetime.strptime(InputD[item][0:7],"%I:%M%p")
                                except ValueError:
                                    getDateTime=datetime.now().replace(microsecond=0)
                                    getDate=getDateTime.date()
                                    getTime=getDateTime.time()
                                    getDate=str(getDate)
                                    getTime=str(getTime)
                                    Date=datetime.strptime(getDate,"%Y/%m/%d")
                                    Time=datetime.strptime(getTime,"%H:%M%S")

                    ExData=[TruckId,Gross,Time,Date]

                    SetSQL=SQL.SQL_IN(ExData)
                    SetPrinterIn=PrinterConnect.Printer(PrinterPort,True,printerDataIn)
                    print(TruckId)
                    print(Gross)
                    print(Date)
                    print(Time)
                    return Mode
                #WeigghOut Mode
                elif dataSize>100:
                    #set weighout mode
                    printerDataOut=SerialData
                    print("Weigh Out")
                    Gross=""
                    Net=""
                    Tare=""
                    Mode="WEIGH OUT"
                    for item in range(len(InputD)+1):
        
                        match item:
                            case 0:
                                TruckId=InputD[item][10:]    
                            
                            case 2:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:
                                        Gross+=word

                            case 3:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:
                                        Tare+=word
                            
                            case 4:
                                start=InputD[item]

                                for letter in range(len(start)):
                                    word=str(start[letter])
                                    #print(middle)
                                    search=word.isnumeric()
                                    if search:  
                                        Net+=word
                            
                            case 6:
                                try:
                                    Date=datetime.strptime(InputD[item][8:],"%m/%d/%Y")
                                    Time=datetime.strptime(InputD[item][0:7],"%I:%M%p")
                                except ValueError:
                                    getDateTime=datetime.now().replace(microsecond=0)
                                    getDate=getDateTime.date()
                                    getTime=getDateTime.time()
                                    getDate=str(getDate)
                                    getTime=str(getTime)
                                    Date=datetime.strptime(getDate,"%Y/%m/%d")
                                    Time=datetime.strptime(getTime,"%H:%M%S")
                                
                    ExData=[TruckId,Gross,Tare,Net,Time,Date]
                    LoggerInfo.info("Mode:%s",Mode)
                    LoggerInfo.info("SQL DATA:%s",ExData)
                    SetSQL=SQL.SQL_OUT(ExData)
                    SetPrinterOut=PrinterConnect.Printer(PrinterPort,True,printerDataOut)

                    print(TruckId)
                    print(Gross)
                    print(Tare)
                    print(Net)
                    print(Date)
                    print(Time)

                    return Mode

            
        
            # Remove all data in the read buffer
            ConnectScale.reset_input_buffer() 

    #Close Scale and Excel file
    ConnectScale.close










