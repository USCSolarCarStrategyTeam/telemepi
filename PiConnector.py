__author__ = 'YutongGu'

import socket
import threading
from SCPiDisplay import *

class Connector:
    HOST='10.120.60.40'
    PORT=13000
    message=''
    connected=False
    input=''
    TIMEOUT=15
    sock=object
    #should move this somewhere else


    def __init__(self, data):
        # set up the SPI interface pins
        self.datalist=data

        pass

        # 10k trim pot connected to adc #0

    def startclient(self):
        #set up socket
        try:
            #create an AF_INET, STREAM socket (TCP)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.TIMEOUT)
        except:
            print 'Failed to create socket'
        try:
            self.sock.connect((self.HOST,self.PORT))
            self.connected=True
            print('connection established')
        except:
            print('connection cannot be established')
            
            pass

        try:
            thread2 = threading.Thread(target=self.transmitData, args=())
            thread2.daemon = True
            thread2.start()
        except:
            print('failed to thread transmitData')

    def transmitData(self):
        failedAttempts=0
        
        while self.connected:
            message=""
            try:
                polling=self.sock.recv(16)
            except socket.timeout:
                print("Connection timed out. Disconnected")
                self.closeserv()
                break

            if(polling=="poll"):
                for x in self.value_names:
                    message=message+x+':'+str(self.datalist.data[x])+';'
                message=message[:-1]
                print message
                if(failedAttempts>=100):
                    self.closeserv()
                    break
                try:
                    self.sock.sendall(message)
                except:
                    print('sending data failed.')
                    failedAttempts+=1

    def closeserv(self):
        if(self.connected == True):
            try:
                self.sock.sendall("quit")
            except:
                print 'connection already closed'
            self.sock.close()
            self.connected=False

    def closeall(self):
        self.closeserv()
        self.keepsampling=False

    # change these as desired - they're the pins connected from the
    # SPI port on the ADC to the Cobbler


