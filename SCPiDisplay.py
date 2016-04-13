__author__ = 'YutongGu'

from PiConnector import *
from Tkinter import *
from Datalists import Datalists
from PiReader import valueReader
import datetime
#!/usr/bin/env python
# -*- coding: utf-8 -*-

FILL1="#008080"
FILL2="#00b3b3"
FILL3="#00e6e6"
FILL4="#1affff"
FILL5="#99ffff"
FILL6="#ccffff"
BAD="#ff9980"
WARN="#ffffb3"
GOOD="#33cc33"

class Display():

    w1=Label()
    w2=Label()
    w3=Label()
    w4=Label()
    w5=Label()
    w6=Label()
    timeLabel=Label()
    labels={"cabintemp":w1,"motortemp":w2,"batterytemp":w3,"motorrpm":w4,"solarvolt":w5,"batvolt":w6}
    UPDATESPEED_MS=100
    batteryX1=0
    batteryX2=0
    batteryY1=0
    batteryY2=0
    height=0
    chargedrainratio=0.5

    def quit(self):
        self.connector.closeall()
        self.reader.quit()
        print "connector"
        self.master.quit()
        

    def connect(self):

        if(self.connector.connected==False):
            print('Trying to connect')
            self.connector.startclient()
        else:
            print('Already connected!')
        pass

    def disconnect(self):

        if(self.connector.connected==True):
            print("Trying to close")
            self.connector.closeserv()
        else:
            print("Already closed")

        pass

    def update(self):
        localtime=datetime.datetime.now().strftime('%H:%M')
        self.timeLabel.config(text=localtime)

        keys=self.datalist.data.keys()
        for i in keys:
            color=WARN
            value=self.datalist.data[i]
            if(i=="motorrpm" or i=="batvolt"):
                self.labels[i].config(text=str(value)+self.datalist.dataunits[i])
                continue
            if(value<self.datalist.databounds[i][0]):
                color=self.datalist.datarules[i][0]
            elif(value<self.datalist.databounds[i][1]):
                color=self.datalist.datarules[i][1]
            elif(value<self.datalist.databounds[i][2]):
                color=self.datalist.datarules[i][2]
            elif(value<self.datalist.databounds[i][3]):
                color=self.datalist.datarules[i][3]
            else:
                color=self.datalist.datarules[i][4]
            self.labels[i].config(text=str(value)+self.datalist.dataunits[i], bg=color)


        self.batterydisplay.delete("level")
        self.chargedisplay.delete("level")

        #updating chargedischargeratio (will eventually change for more accurate model)
        total=self.datalist.data["solarvolt"]+self.datalist.data["motorrpm"]
        if(total==0):
            self.chargedrainratio=0.5
        else:
             self.chargedrainratio=(self.datalist.data["solarvolt"]*1.0/(total))

        color=GOOD
        if(self.chargedrainratio<0.4):
            color=BAD
        elif(self.chargedrainratio<0.6):
            color=WARN
        self.chargedisplay.create_rectangle(5, 7, (self.chargedisplay.winfo_reqwidth()-10)*self.chargedrainratio+5, self.chargedisplay.winfo_reqheight()-7, fill=color, width=2, tag="level")

        color=GOOD
        if(self.datalist.data["batvolt"]<15):
            color=BAD
        elif(self.datalist.data["batvolt"]<40):
            color=WARN
        self.batterydisplay.create_rectangle(self.batteryX1, (self.batteryY2-(self.height*self.datalist.data["batvolt"]/100)), self.batteryX2, self.batteryY2,fill=color, tag="level")



        self.master.after(self.UPDATESPEED_MS, self.update)
        pass
                

    def __init__(self):
        print('starting')
        WIDTH=600
        HEIGHT=350
        
        self.datalist=Datalists()
        self.connector=Connector(self.datalist)
        self.reader=valueReader(self.datalist)
        self.master = Tk()
        self.master.geometry(str(WIDTH)+"x"+str(HEIGHT+25))
        self.master.title("SCSC Racing Telemetry")


        timeframe=Frame(self.master, height=25, width=WIDTH, bg=FILL1)
        timeframe.pack_propagate(0)
        timeframe.grid(row=0, columnspan=3)

        speedframe=Frame(self.master, height=2*HEIGHT/5, width=WIDTH/2, bg=FILL2)
        speedframe.grid_propagate(0)
        speedframe.grid(row=1, column=0)

        statsframe=Frame(self.master, height=2*HEIGHT/5, width=WIDTH/2, bg=FILL3)
        statsframe.grid_propagate(0)
        statsframe.grid(row=2, column=0)

        batteryframe=Frame(self.master, height=4*HEIGHT/5, width=3*WIDTH/8, bg=FILL4) #blue-ish
        batteryframe.grid_propagate(0)
        batteryframe.grid(row=1, column=1, rowspan=2)

        errorframe=Frame(self.master, height=4*HEIGHT/5, width=WIDTH/8)
        errorframe.grid_propagate(0)
        errorframe.grid(row=1, column=2, rowspan=2)

        chargeframe=Frame(self.master, height=HEIGHT/10, width=WIDTH, bg=FILL5)
        chargeframe.grid_propagate(0)
        chargeframe.grid(row=3, columnspan=3)

        buttonframe=Frame(self.master, height=HEIGHT/10, width=WIDTH, bg=FILL6)
        buttonframe.grid_propagate(0)
        buttonframe.grid(row=4, columnspan=3)

        label = Label(statsframe, text="Cabin Temperature:", anchor=W, wraplength=WIDTH/7,bg=FILL3, justify=LEFT,
                         font=("Helvetica", 9, "bold"), padx=10)
        label.grid(row=0)
        self.labels["cabintemp"] = Label(statsframe, text="0"+str(self.datalist.dataunits["cabintemp"]), anchor=W,bg=FILL3, font=("Helvetica", 16))
        self.labels["cabintemp"].grid(row=0,column=1)

        label = Label(statsframe, text="Motor Temperature:", anchor=W, wraplength=WIDTH/7,bg=FILL3, justify=LEFT,
                         font=("Helvetica", 9, "bold"), padx=10)
        label.grid(row=1)
        self.labels["motortemp"] = Label(statsframe, text="0"+str(self.datalist.dataunits["motortemp"]), anchor=W,bg=FILL3, font=("Helvetica", 16))
        self.labels["motortemp"].grid(row=1,column=1)

        label = Label(statsframe, text="Battery Temperature:", anchor=W, wraplength=WIDTH/7,bg=FILL3, justify=LEFT,
                         font=("Helvetica", 9, "bold"), padx=10)
        label.grid(row=1, column=2)
        self.labels["batterytemp"] = Label(statsframe, text="0"+str(self.datalist.dataunits["batterytemp"]), anchor=W,bg=FILL3, font=("Helvetica", 16))
        self.labels["batterytemp"].grid(row=1,column=3)

        label = Label(speedframe, text="Motor RPM:", width=WIDTH/16, anchor=W, bg=FILL2,
                         font=("Helvetica", 12, "bold"), padx=10)
        label.grid(row=0, column=0)
        self.labels["motorrpm"] = Label(speedframe, text="0"+str(self.datalist.dataunits["motorrpm"]),width=WIDTH/80,anchor=W,bg=FILL2, font=("Helvetica", 48), padx=10)
        self.labels["motorrpm"].grid(row=1, column=0, sticky=W)

        label = Label(statsframe, text="Solar Panel Voltage:", anchor=W, wraplength=WIDTH/7,bg=FILL3, justify=LEFT,
                         font=("Helvetica", 9, "bold"), padx=10)
        label.grid(row=0, column=2)
        self.labels["solarvolt"] = Label(statsframe, text="0"+str(self.datalist.dataunits["solarvolt"]), anchor=W,bg=FILL3, font=("Helvetica", 16))
        self.labels["solarvolt"].grid(row=0,column=3)

        label = Label(batteryframe, text="Battery Voltage:", height=1, width=WIDTH/16, anchor=W, bg=FILL4,
                         font=("Helvetica", 12, "bold"), padx=10)
        label.grid(row=0, columnspan=2)
        self.labels["batvolt"] = Label(batteryframe, text="0"+str(self.datalist.dataunits["batvolt"]), bg=FILL4, font=("Helvetica", 24), pady=HEIGHT/40) #blue-ish
        self.labels["batvolt"].grid(row=1, column=0, sticky=E)

        localtime=datetime.datetime.now().strftime('%H:%M')
        self.timeLabel=Label(timeframe, text=localtime, bg=FILL1, font=("Helvetica", 12, "bold"), anchor=E, padx=10)
        self.timeLabel.pack(side=RIGHT )

        b1 =Button(buttonframe, text="Connect",width=20, command=self.connect)
        b1.grid(row=0,column=0,sticky=E)
        b2 =Button(buttonframe, text="Disconnect",width=20, command=self.disconnect)
        b2.grid(row=0,column=1,sticky=W)

        self.batterydisplay=Canvas(batteryframe, bg=FILL4, highlightthickness=0, width=batteryframe.winfo_reqwidth()/2, height=batteryframe.winfo_reqheight()-25) #blue-ish
        self.batteryX1=self.batterydisplay.winfo_reqwidth()/4
        self.batteryY1=self.batterydisplay.winfo_reqheight()/8
        self.batteryX2=3*self.batterydisplay.winfo_reqwidth()/4
        self.batteryY2=7*self.batterydisplay.winfo_reqheight()/8
        self.height=self.batteryY2-self.batteryY1
        self.batterydisplay.create_rectangle(self.batteryX1, self.batteryY1, self.batteryX2, self.batteryY2, outline="BLACK", width=2)
        self.batterydisplay.create_rectangle(self.batteryX1, (self.batteryY2-(self.height*self.datalist.data["batvolt"]/100)), self.batteryX2, self.batteryY2,fill=WARN, tag="level")
        self.batterydisplay.grid(row=1,column=1)

        label= Label(chargeframe, text="Charging meter:", font=("Helvetica", 12, "bold"), anchor=W, bg=FILL5, justify=LEFT, padx=10)
        label.grid(row=0, column=0)
        self.chargedisplay=Canvas(chargeframe, bg=FILL5, highlightthickness=0, width=chargeframe.winfo_reqwidth()*3/4, height=chargeframe.winfo_reqheight())
        self.chargedisplay.grid(row=0, column=1)
        self.chargedisplay.create_rectangle(5,7,self.chargedisplay.winfo_reqwidth()-5,self.chargedisplay.winfo_reqheight()-7, width=2)
        self.chargedisplay.create_line(self.chargedisplay.winfo_reqwidth()/2,7, self.chargedisplay.winfo_reqwidth()/2,0, width=2)
        self.chargedisplay.create_rectangle(5, 7, (self.chargedisplay.winfo_reqwidth()-10)*self.chargedrainratio+5, self.chargedisplay.winfo_reqheight()-7, fill=WARN, width=2, tag="level")

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
