'''
Created on 01.05.2014

@author: drakonkn
'''
from PyQt4 import QtGui
from PyQt4.QtGui import QListWidgetItem
from PyQt4.Qt import QRect, QXmlStreamWriter, QString, QXmlStreamReader,\
    QTextCodec
from PyQt4 import QtCore


class MainWindow(QtGui.QWidget):
    sendMessage = QtCore.pyqtSignal(QString)
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.history = QtGui.QListWidget(self)
        self.message = QtGui.QTextEdit("Type message here",self)
        self.history.setGeometry(QRect(10,10,300,100))
        self.message.setGeometry(QRect(10, 120,300,100))
        self.sendButton = QtGui.QPushButton(u"Send",self)
        self.sendButton.setGeometry(QRect(250,230,50,30))
        self.sendButton.clicked.connect(self.onSendClicked)
        self.history.setAlternatingRowColors(1)
        self.nickName = QtGui.QLineEdit("NickName",self)
        self.nickName.setGeometry(QRect(10,230,200,30))
        
    def getMessage(self,st):
        print "get: "+st
        xml = QXmlStreamReader(st)
        while not xml.atEnd():
            if xml.name().toString() == "message":
                nick = xml.attributes().value("nickName").toString()
                message = xml.readElementText()
            xml.readNext()
        codec = QTextCodec.codecForName("UTF-8");
        stringu = codec.toUnicode(message);
        self.history.addItem(QListWidgetItem(nick+" say:\n"+stringu))  
        
    def onSendClicked(self):
        message = self.message.toPlainText()
        if message != "":
            res = QString()
            xml = QXmlStreamWriter(res);
            #::codecForName("KOI8-R");
            #QString string = codec->toUnicode(encodedString);
            xml.setCodec(QTextCodec.codecForName("UTF-8"))
            xml.writeStartDocument()
            xml.writeStartElement("message")
            xml.writeAttribute("nickName", self.nickName.text())
            xml.writeCharacters(self.message.toPlainText())
            xml.writeEndElement()
            #print("mw send "+res)
            self.message.clear()
            self.sendMessage.emit(res)
            
            
            