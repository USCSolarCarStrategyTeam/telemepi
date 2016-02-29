__author__ = 'YutongGu'

import PiConnector
from Tkinter import *

class SCPiDisplay():
    isConnected=False
    connect=object;

    def run(self):
        global connect
        connect= PiConnector()


    def on_stop(self):
        global connect
        connect.close()
        print("Successfully closed")
        sys.exit();
        #App.stop()

if __name__ == '__main__':
    SCPiDisplay().run()