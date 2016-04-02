#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
        pass
