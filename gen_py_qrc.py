#!/usr/bin/env python

# Helper script that compiles the Qt Resources file into an importable python
# module
import subprocess
subprocess.call("rcc -g python tor-util.qrc > tor_util/tor_util_qrc.py",shell=True)
subprocess.call("sed -i s/PySide2/PyQt5/g tor_util/tor_util_qrc.py",shell=True)
