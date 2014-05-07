'''
Created on 30.04.2014

@author: drakonkn
'''
from PyQt4 import QtNetwork, QtCore
from PyQt4.Qt import QObject

class Network(QtCore.QObject):
    groupAddress = QtNetwork.QHostAddress("224.2.2.5");
    messageReady = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        QObject.__init__(self,parent)
        self.initSockets()

    def initSockets(self):
        self.udpSocketOut = QtNetwork.QUdpSocket(self);
        self.udpSocketOut.bind(self.groupAddress, 45454,QtNetwork.QUdpSocket.ShareAddress)
        self.udpSocketOut.joinMulticastGroup(self.groupAddress)
        self.udpSocketIn = QtNetwork.QUdpSocket(self);
        self.udpSocketIn.bind(self.groupAddress, 45454,QtNetwork.QUdpSocket.ShareAddress)
        self.udpSocketIn.joinMulticastGroup(self.groupAddress)
        self.udpSocketIn.readyRead.connect(self.onGetMessage)

    def onGetMessage(self):
        size = -1
        if self.udpSocketIn.hasPendingDatagrams:
            size = self.udpSocketIn.pendingDatagramSize()
        res = str()
        while size > 0:
            print("rev: "+str(size))
            res = self.udpSocketIn.readDatagram(size)[0]
            if self.udpSocketIn.hasPendingDatagrams:
                size = self.udpSocketIn.pendingDatagramSize()
            else :
                size = -1
        print("Get message:"+str(res))
        self.messageReady.emit(str(res))
        
    def sendMessage(self,message):
        #print("try to send"+message)
        self.udpSocketOut.writeDatagram(message, self.groupAddress, 45454)
        #print("SenD:"+str(sended))
        self.udpSocketOut.flush()
        
        
        