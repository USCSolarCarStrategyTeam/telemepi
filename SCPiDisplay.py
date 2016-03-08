__author__ = 'YutongGu'

from PiConnector import *
from Tkinter import *
import time
from Datalists import Datalists


class Display():
    
    w1=Scale()
    w2=Scale()
    w3=Scale()
    w4=Scale()
    w5=Scale()
    w6=Scale()
    scales=[w1,w2,w3,w4,w5,w6]

    def quit(self):
        connect.closeall()

    def connect(self):
        if(connect.connected==False):
            connect.startclient()
            print('Successfully connected!')
        else:
            print('Already connected!')
            
    def update(self):
            x=0
            values=self.datalist.data.values()
            print values
            for i in values:
                self.scales[x].set(i)
                self.scales[x].pack()
                x=x+1
            self.master.after(500, self.update)
                
    def disconnect(self):
        if(connect.connected==True):
            connect.closeserv()
            print("Successfully closed")
        else:
            print("Already closed")
        sys.exit()
        #App.stop()

    def __init__(self):
        print('starting')
        global connect
        self.datalist=Datalists()
        connect=Connector(self.datalist)
        self.master = Tk()
        w1_label = Label(self.master, text="cabintemp")
        w1_label.pack()
        self.scales[0] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[0].pack()
        self.scales[0].set(0)
        w2_label = Label(self.master, text="solarvolt")
        w2_label.pack()
        self.scales[1] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[1].pack()
        self.scales[1].set(0)
        w3_label = Label(self.master, text="batvolt")
        w3_label.pack()
        self.scales[2] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[2].pack()
        self.scales[2].set(0)
        w4_label = Label(self.master, text="batterytemp")
        w4_label.pack()
        self.scales[3] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[3].pack()
        self.scales[3].set(0)
        w5_label = Label(self.master, text="motorrpm")
        w5_label.pack()
        self.scales[4] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[4].pack()
        self.scales[4].set(0)
        w6_label = Label(self.master, text="motortemp")
        w6_label.pack()
        self.scales[5] = Scale(self.master, from_=0, to=100, orient=HORIZONTAL)
        self.scales[5].pack()
        self.scales[5].set(0)
        w7 =Button(self.master, text="Connect", command=self.connect)
        w7.pack()
        w7 =Button(self.master, text="Disconnect", command=self.disconnect)
        w7.pack()
        self.update()
        self.master.protocol("WM_DELETE_WINDOW", quit)
        self.master.mainloop()



if __name__ == '__main__':
   Display()
