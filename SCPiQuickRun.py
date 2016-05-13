__author__ = 'YutongGu'
from PiConnector import *
from PiReader import *
from Datalists import *

#just a way to start the program w/out a GUI and all on the terminal
def main():
    datalist = Datalists()
    reader = valueReader(datalist)
    connector = Connector(datalist)
    try:
        while(True):
            print datalist.getdatastring()
            time.sleep(1)
    except KeyboardInterrupt:
        connector.closeall()
        reader.quit()

if __name__== "__main__":
    main()
