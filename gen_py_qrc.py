#!/usr/bin/env python

# Helper script that compiles the Qt Resources file into an importable python
# module
import subprocess
print("Compiling tor-util icon file")
subprocess.call("rcc -g python tor-util.qrc > tor_util/tor_util_qrc.py",shell=True)

## Replace PySide with PyQT, because we use PyQt in this project

#subprocess.call("sed -i s/PySide2/PyQt5/g tor_util/tor_util_qrc.py",shell=True)
# sed re-implemented natively in python to avoid compatibility issues
# with platforms that don't support sed natively.
f = open("tor_util/tor_util_qrc.py","r")
contents = f.read()
f.close()
contents = contents.replace("PySide2","PyQt5")
f =  open("tor_util/tor_util_qrc.py","w")
f.write(contents)
f.close()
