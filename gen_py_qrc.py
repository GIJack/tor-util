#!/usr/bin/env python

# Helper script that compiles the Qt Resources file into an importable python
# module
import subprocess
print("Compiling tor-util icon file")
subprocess.call("rcc -g python tor-util.qrc > tor_util/tor_util_qrc.py",shell=True)
subprocess.call("sed -i s/PySide2/PyQt5/g tor_util/tor_util_qrc.py",shell=True)
