#!/usr/bin/env python
tor_util_desc='''
This is a utility for controling TOR via the API. It does two things.
1. Send commands to the API over the network
2. Generates hashed passwords for use in the torrc file

So far, the only commmand supported is NEWNYM, which generates a new
Path, resulting in new exit node, and new IP for TOR connection
'''
tor_util_desc = tor_util_desc.strip()

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication


def main():
    app = QApplication(sys.argv)

    # Main Window
    global window
    widget = uic.loadUi("tor-util.ui")
    
    # Button Presses go here:
    
    widget.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
   main()
