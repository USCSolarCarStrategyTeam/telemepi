__author__ = 'YutongGu'

import RPi.GPIO as GPIO
import time
import threading

class valueReader:
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = [25, 4] #selects the adc converter to read from
    tolerance = 10
    SAMPLESPEED_S = 0.05
    keepsampling = True

    potentiometer_adc = [0, 1, 2, 8] #determine pins to read from.
    #Value will be modulused to get a valid adc location.
    #Value will be divided by 8 and rounded down to get a valid index for SPICS chip select

    trim_pot = [0]*len(potentiometer_adc) #where raw data will be stored
    last_read = [0]*len(potentiometer_adc) #this keeps track of the last potentiometer value
    set_value = [0]*len(potentiometer_adc) #where converted value will be stored
    return_value = [0]*len(potentiometer_adc) #where actual value to return will be stored
    
    pot_adjust = [0]*len(potentiometer_adc)

    #initializes valueReader with a datalist to edit on
    def __init__(self, data):

        self.datalist = data

        #setting up the GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS[0], GPIO.OUT)
        GPIO.setup(self.SPICS[1], GPIO.OUT)
	print 'GPIO set up'

        #start sampling
        try:
            thread1 = threading.Thread(target=self.sample, args=())
            thread1.daemon = True
            thread1.start()
        except:
            print 'failed to thread sample'


    #deconstructor
    def __del__(self):
        if(self.keepsampling==True):
            print "PiReader deconstructed"
            self.quit()
        pass

    #sampling from the adc converters
    #Note: potentiometer values will be stored in the order that Datalists.value_names are listed in Datalists.py
    #ie, pin 0 -> motorrpm, pin 1 -> solarvolt, pin 2 -> batvolt, pin 8 -> motortemp
    def sample(self):

        while self.keepsampling:

            #reading the analog pins
            for x in range(0, len(self.potentiometer_adc)):
                self.trim_pot[x] = self.readadc(self.potentiometer_adc[x]%8, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS[self.potentiometer_adc[x]/8]) #read the value from the ADC

                # how much has it changed since the last read?
                self.pot_adjust[x] = abs(self.trim_pot[x] - self.last_read[x])

                if self.pot_adjust[x] > self.tolerance:
                    self.set_value[x] = self.trim_pot[x] / self.datalist.adcconversionfactor[self.datalist.value_names[x]]  # convert 10bit adc0 (0-1024) trim pot read into appropriate level
                    self.return_value[x] = round(self.set_value[x])          # round out decimal value
                    self.return_value[x] = int(self.return_value[x])            # cast volume as integer
                    self.last_read[x] = self.trim_pot[x]
                    self.updateData(x)
            time.sleep(self.SAMPLESPEED_S)
        pass

    #updates the value based on the index it corresponds to in Datalist.value_names
    def updateData(self, i):
        self.datalist.data[self.datalist.value_names[i]] = self.return_value[i]
        pass

    # read SPI data from MCP3008 chip, 8 possible pins (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if adcnum > 7 or adcnum < 0:
                return -1

        GPIO.output(cspin, True)
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        #lots of binary arithmatic, don't worry about it too much
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if commandout & 0x80:
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

    def quit(self):
        self.keepsampling=False
        GPIO.cleanup()
        pass
