#!/usr/bin/env python
tor_util_desc='''
This is a utility for controling TOR via the API. This is the GUI
version written with Qt5

It does two things:
1. Send commands to the API over the network
2. Generates hashed passwords for use in the torrc file

Network Settings are stored in ~/.config/tor_util/config

API Commands Available:
New IP  - Sends SIGNAL NEWNYM, which regenerates path through the TOR
Network, and gets a new exit node, with a new IP.

Flush DNS - Sends SIGNAL CLEARDNSCACHE, which clears cached DNS lookups.
Use with troubleshooting.

Dormant Mode - Puts the TOR Daemon in dormant mode. New feature that
reduces resource consumption.

'''
tor_util_desc = tor_util_desc.strip()

from tor_util_lib import *

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QObject, QThread, QThreadPool, pyqtSlot, pyqtSignal

def populate_send_options():
    '''populate the action combo box'''
    for item in send_commands:
       widget.combo_action_send.addItem(item)

def final_cleanup():
    '''Cleanup before exit'''
    config = get_send_opts()
    write_config(conf_file,config)

def get_send_opts():
    '''get options from GUI and return them as a dict{}'''
    config = {}
    config['tor_host'] = widget.text_host_send.text()
    config['password'] = widget.text_password_send.text()
    
    try:
        config['tor_port'] = int( widget.text_port_send.text() )
    except:
        config['tor_port'] = default_config['tor_port']
        
    return config

class send_action(QObject):
    '''This is what happens when send button is pressed'''
    finished = pyqtSignal()
    
    def run(self):
        config = get_send_opts()
        action = widget.combo_action_send.currentText()
    
        # Do function
        if action == "New IP":
            command = "SIGNAL NEWNYM"
            widget.text_output_send.appendPlainText("* Sending New IP Request...")
        elif action == "Flush DNS":
            widget.text_output_send.appendPlainText("* Clearing DNS Cache...")
            command = "SIGNAL CLEARDNSCACHE"
        elif action == "Dormant Mode":
            widget.text_output_send.appendPlainText("* Putting TOR Daemon in Dormant Mode...")
            command = "SIGNAL DORMANT"
        elif action == "Active Mode":
            widget.text_output_send.appendPlainText("* Restoring TOR Daemon to Active Mode...")
            command = "SIGNAL ACTIVE"
        elif action == "TOR Version":
            widget.text_output_send.appendPlainText("* Querying TOR Daemon Version:")
            command = "GETINFO version"
        else:
            widget.text_output_send.appendPlainText(action + " Unsupported")
            return
        result = send_tor_new_ip(command,config['tor_host'],config['tor_port'],config['password'])
        output = ""
    
        for line in result:
            error_code = int(line[0])
            output += " ".join(line[1:])
            output  = output.strip("-")
            output  = output.strip()
        if error_code != 250:
            output = "ERROR: " + output
        
        output += "\n"
        widget.text_output_send.appendPlainText(output)
        self.finished.emit()
    
def clear_output_boxes():
    '''Clear Output on button press'''
    widget.text_output_send.setPlainText('')
    widget.text_output_hash.setPlainText('')
    widget.text_password_hash.setText('')

def main():
    app = QApplication(sys.argv)

    # Main Window
    global widget
    widget = uic.loadUi("tor-util.ui")
    
    # thread
    widget.thread = QThread()
    widget.send_worker = send_action()
    widget.send_worker.moveToThread(widget.thread)
    widget.thread.started.connect(widget.send_worker.run)
    widget.send_worker.finished.connect(widget.thread.quit)
    widget.send_worker.finished.connect(widget.send_worker.deleteLater)
    widget.send_worker.finished.connect(widget.thread.deleteLater)
    
    # Button Presses go here:
    widget.action_api_send.triggered.connect(widget.thread.start)
    widget.action_clear_display.triggered.connect(clear_output_boxes)
    
    # Misc effects:
    widget.action_exit_cleanup.triggered.connect(final_cleanup)
    
    # Initialization
    widget.label_name.setText(prog_meta['name'])
    widget.label_version.setText(prog_meta['version'])
    populate_send_options()
    
    # Load Config
    try:
        config = proc_config_start()
    except:
        widget.text_output_send.appendPlainText("** Warning: ¡Could not load config!, using defaults...")
        config = default_config
            
    widget.text_host_send.setText(config['tor_host'])
    widget.text_port_send.setText( str(config['tor_port']) )
    widget.text_password_send.setText(config['password'])
    
    widget.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
   main()
