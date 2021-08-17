#!/usr/bin/env python

# Helper script that compiles the Qt Resources file into a python module
# run this every time the .qrc file is changed
import subprocess
print("Compiling tor-util icon file")

contents = subprocess.check_output(["rcc", "-g", "python", "tor-util.qrc"])
contents = contents.decode()
# Replace PySide with PyQT
contents = contents.replace("PySide2","PyQt5")
f =  open("tor_util/tor_util_qrc.py","w")
f.write(contents)
f.close()
