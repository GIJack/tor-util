#!/usr/bin/env python
tor_util_desc = '''
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

Active Mode - Revives TOR from dormant mode.

TOR Version - Query the daemon for version.

'''
tor_util_desc = tor_util_desc.strip()

send_commands = [ "New IP", "Flush DNS", "Dormant Mode", "Active Mode", "Daemon Status", "TOR Version" ]

from tor_util import common as lib

import traceback
import sys
import os

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        text of result

    progress
        text of progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(
                *self.args, **self.kwargs
            )
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


def populate_send_options():
    '''populate the action combo box'''
    for item in send_commands:
       widget.combo_action_send.addItem(item)


def final_cleanup():
    '''Cleanup before exit'''
    config = get_send_opts()
    lib.write_config(lib.conf_file, config)


def get_send_opts():
    '''get options from GUI and return them as a dict{}'''
    config = {}
    config['tor_host'] = widget.text_host_send.text()
    config['password'] = widget.text_password_send.text()

    try:
        config['tor_port'] = int( widget.text_port_send.text() )
    except:
        config['tor_port'] = lib.default_config['tor_port']

    return config


def send_action(progress_callback):
    '''This is what happens when send button is pressed'''

    config = get_send_opts()
    action = widget.combo_action_send.currentText()

    output = ""
    # Do function
    if action == "New IP":
        command = "SIGNAL NEWNYM"
        output = "* Sending New IP Request..."
    elif action == "Flush DNS":
        output = "* Clearing DNS Cache..."
        command = "SIGNAL CLEARDNSCACHE"
    elif action == "Dormant Mode":
        output = "* Putting TOR Daemon in Dormant Mode..."
        command = "SIGNAL DORMANT"
    elif action == "Active Mode":
        output = "* Restoring TOR Daemon to Active Mode..."
        command = "SIGNAL ACTIVE"
    elif action == "TOR Version":
        output = "* Querying TOR Daemon Version:"
        command = "GETINFO version"
    elif action == "Daemon Status":
        output = "** Checking Status:"
    else:
        output = action + " Unsupported\n"
        return

    progress_callback.emit(output)

    output = ""
    
    if action == "Daemon Status":
        result = lib.tor_daemon_status(config['tor_host'],config['tor_port'],config['password'])
    else:
        result = lib.send_tor_command(command,config['tor_host'],config['tor_port'],config['password'])
    for line in result:
        error_code = int(line[0])
        line = line[-1]
        if error_code != 250:
            output += "ERROR: " + line + "\n"
        else:
            if "=" in line:
                split_line = line.split(" ")
                for line_item in split_line:
                    line_item = line_item.split("=")
                    if len(line_item) == 1:
                        continue
                    output += line_item[0] + ":\t" + line_item[1] + "\n"
            else:
                output += line + "\n"
    return output


def thread_complete():
    widget.button_send.setEnabled(True)


def add_output(add_string):
    widget.text_output_send.appendPlainText(add_string)


def send_button():
    widget.button_send.setEnabled(False)

    # Pass the function to execute
    worker = Worker(send_action)
    worker.signals.finished.connect(thread_complete)
    worker.signals.result.connect(add_output)
    worker.signals.progress.connect(add_output)

    # Execute
    widget.threadpool.start(worker)


def clear_output_boxes():
    '''Clear Output on button press'''
    widget.text_output_send.setPlainText('')
    widget.text_output_hash.setPlainText('')
    widget.text_password_hash.setText('')


def main():
    app = QApplication(sys.argv)

    # Main Window
    global widget
    ui_file = "tor-util.ui"
    if "usr/" in os.path.realpath(__file__) and "bin/" in os.path.realpath(__file__):
        ui_file = "/usr/share/tor-util/tor-util.ui"
    
    widget = uic.loadUi(ui_file)

    # thread
    widget.threadpool = QThreadPool()

    # Button Presses go here:
    widget.action_api_send.triggered.connect(send_button)
    widget.action_clear_display.triggered.connect(clear_output_boxes)

    # Misc effects:
    widget.action_exit_cleanup.triggered.connect(final_cleanup)

    # Initialization
    widget.label_name.setText(lib.prog_meta['name'])
    widget.label_version.setText(lib.prog_meta['version'])
    populate_send_options()

    # Load Config
    try:
        config = lib.proc_config_start()
    except:
        widget.text_output_send.appendPlainText("** Warning: ¡Could not load config!, using defaults...")
        config = lib.default_config

    widget.text_host_send.setText(config['tor_host'])
    widget.text_port_send.setText(str(config['tor_port']))
    widget.text_password_send.setText(config['password'])

    widget.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
   main()
