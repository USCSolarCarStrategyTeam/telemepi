__author__ = 'YutongGu'

#from PiConnector import *
from Tkinter import *
from Datalists import Datalists
#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Display():

    w1=Label()
    w2=Label()
    w3=Label()
    w4=Label()
    w5=Label()
    w6=Label()
    labels=[w1,w2,w3,w4,w5,w6]
    UPDATESPEED_MS=100
    batteryX1=0
    batteryX2=0
    batteryY1=0
    batteryY2=0
    height=0

    def quit(self):
        #self.connector.closeall()
        #print "connector"
        self.master.quit()
        

    def connect(self):
        if(self.connector.connected==False):
            print('Trying to connect')
            self.connector.startclient()
        else:
            print('Already connected!')
        pass

    def update(self):

        x=0
        values=self.datalist.data.values()
        #print values
        for i in values:
            self.labels[x].config(text=str(i)+self.datalist.dataunits[i])
            x=x+1
        self.batterydisplay.delete("level")

        color="GREEN"
        if(self.datalist.data["batvolt"]<15):
            color="RED"
        elif(self.datalist.data["batvolt"]<40):
            color="YELLOW"

        self.batterydisplay.create_rectangle(self.batteryX1, (self.batteryY2-(self.height*self.datalist.data["batvolt"]/100)), self.batteryX2, self.batteryY2,fill=color, tag="level")
        self.master.after(self.UPDATESPEED_MS, self.update)
        pass
                
    def disconnect(self):
        if(self.connector.connected==True):
            print("Trying to close")
            self.connector.closeserv()
        else:
            print("Already closed")
        pass
        #App.stop()

    def __init__(self):
        print('starting')
        WIDTH=700
        HEIGHT=300
        
        self.datalist=Datalists()
        #self.connector=Connector(self.datalist)
        self.master = Tk()
        self.master.geometry(str(WIDTH)+"x"+str(HEIGHT+25)+"+600+200")
        self.master.title("SCSC Racing Telemetry")


        timeframe=Frame(self.master, height=25, width=WIDTH, bg="YELLOW")
        timeframe.grid_propagate(0)
        timeframe.grid(row=0, columnspan=3)

        speedframe=Frame(self.master, height=2*HEIGHT/5, width=WIDTH/2, bg="RED")
        speedframe.grid_propagate(0)
        speedframe.grid(row=1, column=0)

        statsframe=Frame(self.master, height=2*HEIGHT/5, width=WIDTH/2, bg="ORANGE")
        statsframe.grid_propagate(0)
        statsframe.grid(row=2, column=0)

        batteryframe=Frame(self.master, height=4*HEIGHT/5, width=3*WIDTH/8, bg="BLUE")
        batteryframe.grid_propagate(0)
        batteryframe.grid(row=1, column=1, rowspan=2)

        errorframe=Frame(self.master, height=4*HEIGHT/5, width=WIDTH/8)
        errorframe.grid_propagate(0)
        errorframe.grid(row=1, column=2, rowspan=2)

        chargeframe=Frame(self.master, height=HEIGHT/10, width=WIDTH, bg="MAGENTA")
        chargeframe.grid_propagate(0)
        chargeframe.grid(row=3, columnspan=3)

        buttonframe=Frame(self.master, height=HEIGHT/10, width=WIDTH, bg="GREEN")
        buttonframe.grid_propagate(0)
        buttonframe.grid(row=4, columnspan=3)

        w1_label = Label(statsframe, text="Cabin Temperature:", anchor=W, wraplength=WIDTH/7,bg="ORANGE", justify=LEFT,
                         font=("Helvetica", 10), padx=10)
        w1_label.grid(row=0)
        self.labels[0] = Label(statsframe, text="0"+str(self.datalist.dataunits[0]), anchor=W,bg="ORANGE", font=("Helvetica", 16))
        self.labels[0].grid(row=0,column=1)

        w2_label = Label(statsframe, text="Motor Temperature:", anchor=W, wraplength=WIDTH/7,bg="ORANGE", justify=LEFT,
                         font=("Helvetica", 10), padx=10)
        w2_label.grid(row=1)
        self.labels[1] = Label(statsframe, text="0"+str(self.datalist.dataunits[1]), anchor=W,bg="ORANGE", font=("Helvetica", 16))
        self.labels[1].grid(row=1,column=1)

        w3_label = Label(statsframe, text="Battery Temperature:", anchor=W, wraplength=WIDTH/7,bg="ORANGE", justify=LEFT,
                         font=("Helvetica", 10), padx=10)
        w3_label.grid(row=1, column=2)
        self.labels[2] = Label(statsframe, text="0"+str(self.datalist.dataunits[2]), anchor=W,bg="ORANGE", font=("Helvetica", 16))
        self.labels[2].grid(row=1,column=3)

        w4_label = Label(speedframe, text="Motor RPM:", width=WIDTH/16, anchor=W, bg="RED",
                         font=("Helvetica", 12), padx=10)
        w4_label.grid(row=0, column=0)
        self.labels[3] = Label(speedframe, text="0"+str(self.datalist.dataunits[3]),width=WIDTH/80,anchor=W,bg="RED", font=("Helvetica", 48), padx=10)
        self.labels[3].grid(row=1, column=0, sticky=W)

        w5_label = Label(statsframe, text="Solar Panel Voltage:", anchor=W, wraplength=WIDTH/7,bg="ORANGE", justify=LEFT,
                         font=("Helvetica", 10), padx=10)
        w5_label.grid(row=0, column=2)
        self.labels[4] = Label(statsframe, text="0"+str(self.datalist.dataunits[4]), anchor=W,bg="ORANGE", font=("Helvetica", 16))
        self.labels[4].grid(row=0,column=3)

        w6_label = Label(batteryframe, text="Battery Voltage:", height=1, width=WIDTH/16, anchor=W, bg="BLUE",
                         font=("Helvetica", 12), padx=10)
        w6_label.grid(row=0, columnspan=2)
        self.labels[5] = Label(batteryframe, text="0"+str(self.datalist.dataunits[5]), bg="BLUE", font=("Helvetica", 24), pady=HEIGHT/40)
        self.labels[5].grid(row=1, column=0, sticky=E)

        w7 =Button(buttonframe, text="Connect",width=20, command=self.connect)
        w7.grid(row=0,column=0,sticky=E)
        w8 =Button(buttonframe, text="Disconnect",width=20, command=self.disconnect)
        w8.grid(row=0,column=1,sticky=W)

        self.batterydisplay=Canvas(batteryframe, bg="BLUE", highlightthickness=0, width=batteryframe.winfo_reqwidth()/2, height=batteryframe.winfo_reqheight()-25)
        self.batteryX2=3*self.batterydisplay.winfo_reqwidth()/4
        self.batteryY2=7*self.batterydisplay.winfo_reqheight()/8
        self.batteryX1=self.batterydisplay.winfo_reqwidth()/4
        self.batteryY1=self.batterydisplay.winfo_reqheight()/8
        self.height=self.batteryY2-self.batteryY1
        self.batterydisplay.create_rectangle(self.batteryX1, self.batteryY1, self.batteryX2, self.batteryY2, outline="BLACK", width=2)
        self.batterydisplay.create_rectangle(self.batteryX1, (self.batteryY2-(self.height*self.datalist.data["batvolt"]/100)), self.batteryX2, self.batteryY2,fill="GREEN", tag="level")
        self.batterydisplay.grid(row=1,column=1)

        buttonframe.grid_columnconfigure(0, weight=1)
        buttonframe.grid_columnconfigure(1, weight=1)
        statsframe.grid_columnconfigure(0, weight=2)
        statsframe.grid_columnconfigure(1, weight=1)
        statsframe.grid_columnconfigure(2, weight=2)
        statsframe.grid_columnconfigure(3, weight=1)
        statsframe.grid_rowconfigure(0, weight=1)
        statsframe.grid_rowconfigure(1, weight=1)
        speedframe.grid_rowconfigure(0, weight=1)
        speedframe.grid_rowconfigure(1, weight=7)
        batteryframe.grid_columnconfigure(0, weight=1)
        batteryframe.grid_columnconfigure(1, weight=1)

        self.update()
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.master.mainloop()

if __name__ == '__main__':
   Display()
