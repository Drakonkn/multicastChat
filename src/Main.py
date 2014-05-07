# -*- coding: utf-8 -*-
#!/usr/bin/python3.2
#
import sys
from PyQt4 import QtGui
from Net import Net
from Gui import MainWindow
app = QtGui.QApplication(sys.argv)
mw = MainWindow.MainWindow()
mw.show()
net = Net.Network(None)
net.messageReady.connect(mw.getMessage)
mw.sendMessage.connect(net.sendMessage)
app.exec_()
