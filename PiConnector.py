__author__ = 'YutongGu'
import time
import RPi.GPIO as GPIO
from socket import *
import sys
import threading

class PiConnector:
    HOST='10.120.112.75'
    PORT=13000
    message=''
    keepthreading=True
    connected=False
    listening=False
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = 25
    input=''
    potentiometer_adc = [0, 1, 2, 3]
    trim_pot=[0]*len(potentiometer_adc)
    last_read = [0]*len(potentiometer_adc)       # this keeps track of the last potentiometer value
    set_value=[0]*len(potentiometer_adc)
    return_value=[0]*len(potentiometer_adc)
    pot_adjust=[0]*len(potentiometer_adc)
    tolerance = 10
    ftemp=0;

    #should move this somewhere else
    data={'cabintemp': return_value[0],
            'motortemp': return_value[1],
            'batterytemp': return_value[2],
            'motorrpm': 25,
            'solarvolt': ftemp,
            'batvolt': 50
          }

    def __init__(self):
        # set up the SPI interface pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS, GPIO.OUT)
               # to keep from being jittery we'll only change
                            # volume when the pot has moved more than 5 'counts'
        try:
            thread1 = threading.Thread(target=self.sample(), args=())
            thread1.daemon = True
            thread1.start()
        except:
            print 'failed to thread sample'

        #set up socket
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        except socket.error, msg:
            print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit()
        print 'Socket Created'

        self.startclient()

        pass

        # 10k trim pot connected to adc #0

    def startclient(self):
        self.keepthreading=True;
        try:
            self.sock.connect((self.HOST,self.PORT))
            self.connected=True
        except:
            print('connection cannot be established')
            GPIO.cleanup()
            sys.exit(0)
        print('connection established')

        try:
            thread2 = threading.Thread(target=self.transmitData(), args=())
            thread2.daemon = True
            thread2.start()
        except:
            print('failed to thread transmitData')

    def sample(self):

        while self.keepthreading:
            # read the analog pin

            for x in range(0, len(self.potentiometer_adc)):
                self.trim_pot[x] = self.readadc(self.potentiometer_adc[x], self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)

                # how much has it changed since the last read?
                self.pot_adjust[x] = abs(self.trim_pot[x] - self.last_read[x])

                if(self.pot_adjust[x]>self.tolerance):
                    self.set_value[x] = self.trim_pot[x] / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                    self.return_value[x] = round(self.set_value[x])          # round out decimal value
                    self.return_value[x] = int(self.return_value[x])            # cast volume as integer
                    self.last_read[x] = self.trim_pot[x]
            self.ftemp=(self.return_value[3]*1.8)+32
            self.ftemp=round(self.ftemp)
            self.ftemp=int(self.ftemp)
            time.sleep(0.1)

    def transmitData(self):
        self.listening = True
        failedAttempts=0
        message= 'cabintemp:'+str(self.return_value[0])+';solarvolt:'+str(self.return_value[1])+';batvolt:50;batterytemp:'+str(self.ftemp)+';motorrpm:'+str(self.return_value[2])+';motortemp:50'
        while self.keepthreading:
            if(failedAttempts>=100):
                self.keepthreading=False
                self.sock.close()
                break
            try:
                self.sock.sendall(message)
            except:
                print('sending data failed.')
                failedAttempts+=1
                continue
        self.listening = False

    # read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
    def readadc(adcnum, clockpin, mosipin, misopin, cspin):
            if ((adcnum > 7) or (adcnum < 0)):
                    return -1
            GPIO.output(cspin, True)

            GPIO.output(clockpin, False)  # start clock low
            GPIO.output(cspin, False)     # bring CS low

            commandout = adcnum
            commandout |= 0x18  # start bit + single-ended bit
            commandout <<= 3    # we only need to send 5 bits here
            for i in range(5):
                    if (commandout & 0x80):
                            GPIO.output(mosipin, True)
                    else:
                            GPIO.output(mosipin, False)
                    commandout <<= 1
                    GPIO.output(clockpin, True)
                    GPIO.output(clockpin, False)

            adcout = 0
            # read in one empty bit, one null bit and 10 ADC bits
            for i in range(12):
                    GPIO.output(clockpin, True)
                    GPIO.output(clockpin, False)
                    adcout <<= 1
                    if (GPIO.input(misopin)):
                            adcout |= 0x1

            GPIO.output(cspin, True)

            adcout >>= 1       # first bit is 'null' so drop it
            return adcout

    def close(self):
        if(self.connected == True):
            self.keepthreading=False
            self.sock.sendall("quit")
            self.sock.close()

    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler


