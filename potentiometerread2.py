import time
import RPi.GPIO as GPIO
from socket import *
import sys

HOST='10.120.112.75'
PORT=13000
message=''
connected=False
GPIO.setmode(GPIO.BCM)
DEBUG = 0
 
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
 
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

#set up socket
sock=socket(AF_INET, SOCK_STREAM)
 
# 10k trim pot connected to adc #0
potentiometer_adc = [0, 1, 2, 3] 
trim_pot=[0]*len(potentiometer_adc)

last_read = [0]*len(potentiometer_adc)       # this keeps track of the last potentiometer value
set_value=[0]*len(potentiometer_adc)
return_value=[0]*len(potentiometer_adc)
pot_adjust=[0]*len(potentiometer_adc)
tolerance = 10       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

try:
    sock.connect((HOST,PORT))
except:
    print('connection cannot be established')
    GPIO.cleanup()
    sys.exit(0)
print('connection established')

try:
    while True:
        # read the analog pin
        
        for x in range(0, len(potentiometer_adc)):
                trim_pot[x] = readadc(potentiometer_adc[x], SPICLK, SPIMOSI, SPIMISO, SPICS)
                
                # how much has it changed since the last read?
                pot_adjust[x] = abs(trim_pot[x] - last_read[x])
                       
                if(pot_adjust[x]>tolerance):
                        set_value[x] = trim_pot[x] / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                        return_value[x] = round(set_value[x])          # round out decimal value
                        return_value[x] = int(return_value[x])            # cast volume as integer
                        last_read[x] = trim_pot[x]
        ftemp=(return_value[3]*1.8)+32
        ftemp=round(ftemp)
        ftemp=int(ftemp)
        message= 'cabintemp:'+str(return_value[0])+';solarvolt:'+str(return_value[1])+';batvolt:50;batterytemp:'+str(ftemp)+';motorrpm:'+str(return_value[2])+';motortemp:50' 
                
        try:
                sock.sendall(message)
        except:
                print('sending data failed.')
                     
        if DEBUG:
                print "set_volume", set_volume
                print "tri_pot_changed", set_volume
                
        # save the potentiometer reading for the next loop
        
 
        # hang out and do nothing for a half second
        time.sleep(1)
except KeyboardInterrupt:
    print('Keyboard Interrupt')
finally:
    try:
        sock.sendall('quit')
    finally:
        GPIO.cleanup()
        sock.close()
        
