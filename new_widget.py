from PyQt5 import QtCore, QtWidgets
class Set_question:
    def set_return(self,ico,text,dir):  #头像，文本，方向
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widget.setLayoutDirection(dir)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(ico)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setLayoutDirection(QtCore.Qt.LeftToRight)
        if (dir+1)%2:
            self.textBrowser.setStyleSheet("padding:5px;\n"
                                        "background-color: rgba(255,255,255);\n"
                                        "font: 10pt \"微软雅黑\";"
                                        "border-radius: 10px;")
        else:
            self.textBrowser.setStyleSheet("padding:5px;\n"
                                        "background-color: rgba(149,236,109);\n"
                                        "font: 10pt \"微软雅黑\";"
                                        "border-radius: 10px;")
            
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QtCore.QSize(0, 0))

        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout.addWidget(self.textBrowser)


        self.verticalLayout_4.addWidget(self.widget)
