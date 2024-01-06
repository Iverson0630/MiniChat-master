from PyQt5 import QtWidgets , QtCore
from PyQt5.QtWidgets import QApplication,QMainWindow,QMessageBox
import sys
import google.generativeai as genai
from PyQt5.QtCore import QThread,pyqtSignal
from new_widget import Set_question
from PyQt5.QtGui import QFont, QFontMetrics,QPixmap,QIcon
from My_Mainwindow import Ui_MainWindow
from login import Ui_Login
import os
class GetMsg(QThread):
    '''
    arg：
        input
            chat[Gemini]:Gemini对象
            input[str]:输入消息

        output:
            pyqtSignal槽函数
            response[str]:消息回复
    '''
    #自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str)
    # 带一个参数t
    def __init__(self, chat, input , parent=None):
        super(GetMsg, self).__init__(parent)
        self.chat = chat
        self.input = input
    def run(self):
        response = self.chat.send_message(self.input).text
        self.finishSignal.emit(response) 


class MyApp(QMainWindow,Ui_MainWindow):
    def __init__(self,api_key):
        super().__init__()
        self.setupUi(self)
        self.gemini_key = api_key
        self.icon_my = QPixmap("src/my_image")    
        self.icon_gemini = QPixmap("src/gemini.png")  
        self.sum = 1
        self.setWindowIcon(QIcon('src/icon/main.png'))
        self.init_manu()
        self.init_model()
        
        
        self.Button_sendmsg.clicked.connect(self.SendMsg)
        self.Button_file.clicked.connect(self.ChooseFile)
        self.TextEdit_msg.undoAvailable.connect(self.Event)  
        self.scrollArea.verticalScrollBar().rangeChanged.connect(
            lambda: self.scrollArea.verticalScrollBar().setValue(
                self.scrollArea.verticalScrollBar().maximum()
            )
        )

    def Event(self):
        if not self.TextEdit_msg.isEnabled():  #这里通过文本框的是否可输入
            self.TextEdit_msg.setEnabled(True)
            self.Button_sendmsg.click()
            self.TextEdit_msg.setFocus()
            
    def init_manu(self):
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        
        
    def init_model(self):
        genai.configure(api_key=self.gemini_key,transport="rest")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
        model = genai.GenerativeModel('gemini-pro')
        self.chat = model.start_chat(history=[])   
        self.image_chat = genai.GenerativeModel('gemini-pro-vision')
    def ChooseFile(self):
        self.directory = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择保存文件夹")
        

    def SendMsg(self):
        self.msg = self.TextEdit_msg.toPlainText()
        self.TextEdit_msg.clear()
        if len(self.msg)>0:
            self.sum += 1
            self.create_widget ()
            self.set_widget ()

            #self.AddWidget (msg,is_send=True)
            self.threadGetMsg = GetMsg(self.chat, self.msg) 
            self.threadGetMsg.start()
            self.sum += 1
            self.threadGetMsg.finishSignal.connect(self.FinishMsg)

    def FinishMsg(self,msg):
        self.msg = msg
        self.create_widget ()
        self.set_widget ()

    
    
    def create_widget(self):
        
        if self.sum % 2:   # 根据判断创建左右气泡
            Set_question.set_return(self, self.icon_gemini, self.msg, QtCore.Qt.LeftToRight)    # 调用new_widget.py中方法生成左气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列
        else:
            Set_question.set_return(self, self.icon_my, self.msg,QtCore.Qt.RightToLeft)   # 调用new_widget.py中方法生成右气泡
            QApplication.processEvents()                                # 等待并处理主循环事件队列


    # 修改气泡长宽
    def set_widget(self):
        font = QFont()
        font.setPointSize(16)
        fm = QFontMetrics(font)
        text_width = fm.width(self.msg)+115    #根据字体大小生成适合的气泡宽度
        if self.sum != 0:
            if text_width>632:                  #宽度上限
                text_width=int(self.textBrowser.document().size().width())+100  #固定宽度
            self.widget.setMinimumSize(text_width,int(self.textBrowser.document().size().height())+ 40) #规定气泡大小
            self.widget.setMaximumSize(text_width,int(self.textBrowser.document().size().height())+ 40) #规定气泡大小
            self.scrollArea.verticalScrollBar().setValue(10)


class Login(QtWidgets.QMainWindow,Ui_Login):
     #登录界面
     def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)

        if  os.path.exists('src/admin.txt'):
            with open("src/admin.txt", "r") as f:
                data = f.read()
            res = data.split('\n')
            self.admin = res[0]
            self.password = res[1]
            self.plainTextEdit.setPlainText('用户名:'+self.admin)
            self.plainTextEdit_2.setPlainText('密码:******')

     def start(self):
        if  not os.path.exists('src/admin.txt'):
            self.admin = self.plainTextEdit.toPlainText()[5:]
            self.password = self.plainTextEdit_2.toPlainText()[4:]
        import eventlet  # 导入eventlet这个模块,防止未开VPN时连接服务器时卡死
        genai.configure(api_key=self.password,transport="rest")
        count =0

        try:
            eventlet.monkey_patch()  # 必须加这条代码
            with eventlet.Timeout(3, True):  # 设置超时时间为2秒
                for m in genai.list_models():
                    count+=1
        except:
            QMessageBox.warning(self,'错误','网络连接错误', QMessageBox.Yes)
            count =0

        if count>0:
            if self.checkBox.isChecked():
                if not os.path.exists('src/admin.txt'):
                    with open('src/admin.txt', 'w') as f:
                        f.write(self.admin+'\n')
                        f.write(self.password)

            myapp = MyApp(self.password)
            myapp.setWindowTitle("MiniChat")
            #myapp.resize(1470, 820)
            myapp.show()
            self.close()
        else:
            QMessageBox.warning(self,'错误','API_KEY错误', QMessageBox.Yes)


     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

'''
def AddWidget(self,data,is_send):

        label = QtWidgets.QLabel(data)
   
        
        if is_send:
            label.setStyleSheet(
        "QLabel{ font-family: '微软雅黑';font-size: 16px;background-color: #95ec69;border-radius: 10px;}")
            label.setAlignment(QtCore.Qt.AlignRight)
        else:
            label.setStyleSheet(
        "QLabel{ font-family: '微软雅黑';font-size: 16px;background-color: #ffffff;border-radius: 10px;}")
            label.setAlignment(QtCore.Qt.AlignLeft)

        hbox = QtWidgets.QHBoxLayout()
        hbox.addStretch(5)
        hbox.addWidget(label)
        self.verticalLayout_3.addLayout(hbox)
'''