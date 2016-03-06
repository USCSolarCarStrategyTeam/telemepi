__author__ = 'YutongGu'

from PiConnector import Connector
from Tkinter import *

data={'cabintemp': 0,
            'motortemp': 0,
            'batterytemp': 0,
            'motorrpm': 0,
            'solarvolt': 0,
            'batvolt': 0
          }

class Display():
    w1=object
    w2=object
    w3=object
    w4=object
    w5=object
    w6=object
    w7=object
    scales=(w1,w2,w3,w4,w5,w6,w7)

    def run(self):
        if(connect.connected==False):
            connect.startserv()
            print('Successfully connected!')
        else:
            print('Already connected!')


    def quit(self):
        if(connect.connected==True):
            connect.close()
            print("Successfully closed")
        else:
            print("Already closed")
        sys.exit()
        #App.stop()

    def build(self):
        global connect
        connect=Connector()
        master = Tk()
        w1_label = Label(master, text="cabintemp")
        w1_label.pack()
        self.w1 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w1.pack()
        self.w1.set(0)
        w2_label = Label(master, text="solarvolt")
        w2_label.pack()
        self.w2 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w2.pack()
        self.w2.set(0)
        w3_label = Label(master, text="batvolt")
        w3_label.pack()
        self.w3 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w3.pack()
        self.w3.set(0)
        w4_label = Label(master, text="batterytemp")
        w4_label.pack()
        self.w4 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w4.pack()
        self.w4.set(0)
        w5_label = Label(master, text="motorrpm")
        w5_label.pack()
        self.w5 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w5.pack()
        self.w5.set(0)
        w6_label = Label(master, text="motortemp")
        w6_label.pack()
        self.w6 = Scale(master, from_=0, to=100, orient=HORIZONTAL, state=DISABLED)
        self.w6.pack()
        self.w6.set(0)
        w7 =Button(master, text="Connect", command=self.run)
        w7.pack()
        w7 =Button(master, text="Disconnect", command=self.quit)
        w7.pack()

        master.protocol("WM_DELETE_WINDOW", quit)
        master.mainloop()



if __name__ == '__main__':
   Display()