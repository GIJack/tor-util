#!/usr/bin/env python
prog_meta = {
    'name' : "Onion Router API Utility",
    'version' : "0.0.0"
}
tor_util_desc='''
This is a utility for controling TOR via the API. This is the GUI
version written with Qt5

It does two things:
1. Send commands to the API over the network
2. Generates hashed passwords for use in the torrc file

So far, the only commmand supported is NEWNYM, which generates a new
Path, resulting in new exit node, and new IP for TOR connection
'''
tor_util_desc = tor_util_desc.strip()

from tor_util_lib import *

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication

def final_cleanup():
    '''Cleanup before exit'''
    config = {}
    config['tor_host'] = widget.text_host_send.text()
    config['tor_port'] = widget.text_port_send.text()
    config['password'] = widget.text_password_send.text()
    
    write_config(conf_file,config)

def main():
    app = QApplication(sys.argv)

    # Main Window
    global widget
    widget = uic.loadUi("tor-util.ui")
    
    # Button Presses go here:
    
    # Misc effects:
    widget.action_exit_cleanup.triggered.connect(final_cleanup)
    
    # Initialization
    widget.label_name.setText(prog_meta['name'])
    widget.label_version.setText(prog_meta['version'])
    
    # Load Config
    try:
        config = proc_config_start()
    except:
        widget.text_output_send.appendPlainText("** Warning: ¡Could not load config!, using defaults...")
        config = default_config
            
    widget.text_host_send.setText(config['tor_host'])
    widget.text_port_send.setText(config['tor_port'])
    widget.text_password_send.setText(config['password'])
    
    widget.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
   main()
