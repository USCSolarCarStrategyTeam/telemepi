#!/usr/bin/env python
# -*- coding: utf-8 -*-
BAD="#ff9980"
WARN1="#ffbf80"
WARN2="#ffffb3"
WARN3="#c6ff1a"
GOOD="#33cc33"
DESCENDING=[GOOD,WARN1,WARN2,WARN3,BAD]
ASCENDING=[BAD,WARN3,WARN2,WARN1,GOOD]
VALLEY=[GOOD,WARN2,BAD,WARN2,GOOD]
MOUNTAIN=[BAD,WARN2,GOOD,WARN2,BAD]
class Datalists:
    
    def __init__(self):
        self.data={'cabintemp': 0,
            'motortemp': 0,
            'batterytemp': 0,
            'motorrpm':0,
            'solarvolt': 0,
            'batvolt': 0
          }
        self.dataunits={'cabintemp': ' °F',
            'motortemp': ' °F',
            'batterytemp': ' °F',
            'motorrpm': ' rpm',
            'solarvolt': ' V',
            'batvolt': ' V'
          }
        self.databounds={'cabintemp': [20,40,60,80],
            'motortemp': [20,40,60,80],
            'batterytemp': [20,40,60,80],
            'solarvolt': [20,40,60,80],
          }
        self.datarules={'cabintemp': MOUNTAIN,
            'motortemp': DESCENDING,
            'batterytemp': DESCENDING,
            'solarvolt': ASCENDING
          }
        pass
