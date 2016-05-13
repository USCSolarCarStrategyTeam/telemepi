#!/usr/bin/env python
# -*- coding: utf-8 -*-

#predefined colors
GOOD="#33cc33"
WARN3="#ffbf80"
WARN2="#ffffb3"
WARN1="#c6ff1a"
BAD="#ff9980"
#predefined color patterns based on values
DESCENDING=[GOOD,WARN1,WARN2,WARN3,BAD]
ASCENDING=[BAD,WARN3,WARN2,WARN1,GOOD]
VALLEY=[GOOD,WARN2,BAD,WARN2,GOOD]
MOUNTAIN=[BAD,WARN2,GOOD,WARN2,BAD]
class Datalists:


    def __init__(self):
        #values asociated with each data
        self.data={'cabintemp': 0,
            'motortemp': 0,
            'batterytemp': 50,
            'motorrpm': 10,
            'solarvolt': 20,
            'batvolt': 0
          }

        #units that each data is in
        self.dataunits={'cabintemp': ' °F',
            'motortemp': ' °F',
            'batterytemp': ' °F',
            'motorrpm': ' rpm',
            'solarvolt': ' V',
            'batvolt': ' V'
          }

        #bounds for each value that dictate each color change
        self.databounds={'cabintemp': [20,40,60,80],
            'motortemp': [20,40,60,80],
            'batterytemp': [20,40,60,80],
            'solarvolt': [20,40,60,80],
          }

        #rules each value's color change at each bound
        self.datarules={'cabintemp': MOUNTAIN,
            'motortemp': DESCENDING,
            'batterytemp': DESCENDING,
            'solarvolt': ASCENDING
          }

        self.adcconversionfactor={
            'cabintemp': 10.24,
            'motortemp': 10.24,
            'batterytemp': 10.24,
            'motorrpm': 10.24,
            'solarvolt': 10.24,
            'batvolt': 10.24
        }

        #value names
        self.value_names=("motorrpm","solarvolt","batvolt","batterytemp","cabintemp","motortemp")
        pass

    #gets the data in a string form
    def getdatastring(self):
        message=""
        for x in self.value_names:
            message=message+x+':'+str(self.data[x])+' \t '
            message=message[:-1]
        return message