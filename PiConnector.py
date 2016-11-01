__author__ = 'YutongGu'

import socket
import threading
import time

#class is meant for transmitting to a remote computer via sockets over wifi
#will automatically try to connect if disconnected
#print statements make the code pretty self explanatory
class Connector:
    #figure out a better solution eventually
    HOST='empty'


    PORT=13000
    message=''
    connected=False
    statusChanged=False
    input=''
    TIMEOUT=1
    sock=None
    quit=False

    def __init__(self, data):
        self.datalist = data
        try:
            thread1 = threading.Thread(target=self.startclient, args=())
            thread1.daemon = True
            thread1.start()
        except:
            print('failed to thread startclient')
        pass

    def __del__(self):
        if ~self.quit:
            print "PiConnector deconstructed"
            self.closeall()
        pass

    def startclient(self):
        #set up socket
        print "starting client"
        sender=("empty","")
        try:
            self.b = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.b.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.b.settimeout(2)
            print 'Created broadcast socket'
        except socket.error:
            print 'Failed to create broadcast socket'
            return

        while(self.HOST == 'empty'):
            try :
                print 'broadcasting'
                self.b.sendto('message', ('<broadcast>', 9999))
                print 'receiving'
                self.HOST, sender = self.b.recvfrom(1024)

            except socket.error, msg:
                print 'Error Code : ' + str(msg[0])
                #print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            print "Recieved "+self.HOST+" from "+sender[0]
            time.sleep(2)

        print 'Host ip set as: '+self.HOST

        while self.connected==False and ~self.quit:

            print "****************Setting up socket*******************"
            try:
                #create an AF_INET, STREAM socket (TCP)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                self.sock.settimeout(self.TIMEOUT)
            except:
                print 'Failed to create socket'
            self.connect()
            if self.quit:
                break
            time.sleep(10)


    def connect(self):
        try:
            print('***********Trying to connect to '+self.HOST+'*************')
            self.sock.connect((self.HOST,self.PORT))
            self.connected = True
            self.statusChanged=True
            print('***************Connection established***************')
        except:
            self.sock.close()
            del self.sock
            self.sock=None
            print('***************Connection failed********************')
            pass

        try:
            thread2 = threading.Thread(target=self.transmitData, args=())
            thread2.daemon = True
            thread2.start()
        except:
            print('failed to thread transmitData')

    def transmitData(self):
        failedAttempts=0

        while self.connected and ~self.quit:
            message = ""
            try:
                polling=self.sock.recv(16)
            except socket.timeout:
                print("Connection timed out. Disconnected")
                thread3 = threading.Thread(target=self.closeserv, args=())
                thread3.daemon = True
                thread3.start()
                break
            except socket.error:
                print"error"
                thread3 = threading.Thread(target=self.closeserv, args=())
                thread3.daemon = True
                thread3.start()
                break

            if polling == "poll":
                for x in self.datalist.value_names:
                    message = message+x+':'+str(self.datalist.data[x])+';'
                message = message[:-1]
                if failedAttempts >= 50:
                    self.closeserv()
                    break
                try:
                    self.sock.sendall(message)
                except:
                    print('sending data failed.')
                    failedAttempts += 1
            else:
                print"error"
                thread3 = threading.Thread(target=self.closeserv, args=())
                thread3.daemon = True
                thread3.start()
                break
            
    def closeserv(self):
        if self.connected:
            try:
                self.sock.sendall("quit")
            except:
                print 'connection already closed'
            self.sock.close()
            self.connected=False
            self.statusChanged=True
            print "connected set to false***"
            if ~self.quit:
                print "starting client from closeserv"
                self.startclient()

    def closeall(self):
        try:
            self.sock.sendall("quit")
        except:
            print 'couldnt communicate to telemetry'
        self.quit = True
        print "quit set to true***"
        if self.sock is not None:
            self.sock.close()



