__author__ = 'YutongGu'

import RPi.GPIO as GPIO
import time
import threading

class valueReader:
    SPICLK = 18
    SPIMISO = 23
    SPIMOSI = 24
    SPICS = [25,4]
    tolerance = 10
    SAMPLESPEED_S=0.01
    keepsampling=True

    potentiometer_adc = [0, 1, 2, 8] #will be modulused
    trim_pot=[0]*len(potentiometer_adc)
    last_read = [0]*len(potentiometer_adc)       # this keeps track of the last potentiometer value
    set_value=[0]*len(potentiometer_adc)
    return_value=[0]*len(potentiometer_adc)
    
    pot_adjust=[0]*len(potentiometer_adc)

    def __init__(self, data):

        self.datalist=data
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SPIMOSI, GPIO.OUT)
        GPIO.setup(self.SPIMISO, GPIO.IN)
        GPIO.setup(self.SPICLK, GPIO.OUT)
        GPIO.setup(self.SPICS[0], GPIO.OUT)
        GPIO.setup(self.SPICS[1], GPIO.OUT)
        try:
            thread1 = threading.Thread(target=self.sample, args=())
            thread1.daemon = True
            thread1.start()
        except:
            print 'failed to thread sample'

    def sample(self):

        while self.keepsampling:
            # read the analog pin
            #print('sampling')

            for x in range(0, len(self.potentiometer_adc)):
                self.trim_pot[x] = self.readadc(self.potentiometer_adc[x]%8, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS[self.potentiometer_adc[x]/8])

                # how much has it changed since the last read?
                self.pot_adjust[x] = abs(self.trim_pot[x] - self.last_read[x])

                if(self.pot_adjust[x]>self.tolerance):
                    self.set_value[x] = self.trim_pot[x] / 10.24           # convert 10bit adc0 (0-1024) trim pot read into 0-100 volume level
                    self.return_value[x] = round(self.set_value[x])          # round out decimal value
                    self.return_value[x] = int(self.return_value[x])            # cast volume as integer
                    self.last_read[x] = self.trim_pot[x]
                self.updateData()
                time.sleep(self.SAMPLESPEED_S)
        pass

    def updateData(self):
        #print self.datalist.data.values()
        
        for i in range(0, len(self.return_value)):
            self.datalist.data[self.datalist.value_names[i]]=int(self.return_value[i])
        pass

     # read SPI data from MCP3008 chip, 8 possible pins (0 thru 7)
    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
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

    def quit(self):
        self.keepsampling=False
        GPIO.cleanup()
        pass
