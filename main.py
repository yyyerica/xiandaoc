import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QProgressBar
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import untitled2
import difflib
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *  # pyqt 5.10.1版本可用
# sys.path.append('./Pyverilog_develop')  # 重要
import examples
from examples import example_parser
# sys.path.append('./Pyverilog_develop/examples')
# from examples import example_parser
# import Pyverilog_develop
import os
import visualize
# import threading
# sys.path.append('./Pyverilog_develop/examples')
from examples import enhanceone
from examples import ts
from python_riscv import enhanceSecurityTop
import shutil
import trifinder_event_demo

class Thread(QThread):
    def __init__(self):
        super(Thread,self).__init__()

    def run(self):
        # 线程相关的代码
        os.system(r"python3 -m http.server 8099")
    pass


class SecondWindow(QMainWindow):

    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.setWindowTitle('展示窗口')
        self.setGeometry(5, 30, 1500, 1000)


class MainCode(QMainWindow, untitled2.Ui_MainWindow):  # untitled2.Ui_MainWindow

    def __init__(self):
        QMainWindow.__init__(self)
        untitled2.Ui_MainWindow.__init__(self)  # untitled2.Ui_MainWindow
        self.setupUi(self)
        self.setWindowTitle('开源芯片安全检测及优化工具')

        self.prelist = []
        self.basedirpath = os.getcwd()  # /Users/yunyingye/Desktop/desktop/pyqt

        self.button_loadpre.clicked.connect(self.openPreFile)
        self.button_loadpost.clicked.connect(self.openPostFile)

        self.button_clearpre.clicked.connect(self.clearPre)
        self.button_clearpost.clicked.connect(self.clearPost)

        self.button_onepage.clicked.connect(self.showOnePage)
        self.button_twopage.clicked.connect(self.showTwoPage)

        self.tick_win = None
        self.button_compare.clicked.connect(self.compare_file)

        self.button_signal.clicked.connect(self.signalAnalyzePre)
        self.button_signalpost.clicked.connect(self.signalAnalyzePost)

        self.load_prefile.triggered.connect(self.openPreFile)
        self.load_editfile.triggered.connect(self.openPostFile)
        self.signal_enhance.triggered.connect(self.signalEnhance)
        self.zongxian_enhance.triggered.connect(self.zongxianEnhance)
        self.analyzesignal_pre.triggered.connect(self.signalAnalyzePre)
        self.analyzearith_post.triggered.connect(self.signalAnalyzePost)

    def openPreFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "Open files", self.basedirpath+"/Pyverilog-develop/",
                                              options=QFileDialog.DontUseNativeDialog)[0]  # tuple
        self.prelist.clear()
        # print(files) # 绝对路径
        # 用默认的Dialog会自动按文件名对文件列表排序
        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])
            self.list_pre.addItem(item)
            self.prelist.append(file_name)

        self.list_pre.currentItemChanged.connect(self.handlePreChanged)
        self.list_pre.itemClicked.connect(self.showPreCode)

    def openPostFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "Open files", self.basedirpath+"/Pyverilog-develop/",
                                           options=QFileDialog.DontUseNativeDialog)[0]  # tuple

        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document_edit.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])
            self.list_post.addItem(item)

        self.list_post.currentItemChanged.connect(self.handlePostChanged)
        self.list_post.itemClicked.connect(self.showPostode)

    def handlePreChanged(self, current, previous):
        if current != None:
            current.setIcon(QtGui.QIcon(r'./image/document_show.png'))
        if previous != None:
            previous.setIcon(QtGui.QIcon(r'./image/document.png'))

    def handlePostChanged(self, current, previous):
        if current != None:
            current.setIcon(QtGui.QIcon(r'./image/document_show.png'))
        if previous != None:
            previous.setIcon(QtGui.QIcon(r'./image/document_edit.png'))

    def showPreCode(self):
        # print(item.text)
        data = ""
        with open(self.list_pre.selectedItems()[0].whatsThis(), 'r', encoding='utf-8') as f:
            data += f.read()

        self.label.setText(data)
        self.label_2.setText(data)

    def showPostode(self):
        self.showTwoPage()
        data = ""
        with open(self.list_post.selectedItems()[0].whatsThis(), 'r', encoding='utf-8') as f:
            data += f.read()

        self.label_3.setText(data)

    def clearPre(self):
        self.list_pre.clear()
        self.label.setText("")
        self.label_2.setText("")

        self.prelist.clear()

    def clearPost(self):
        self.list_post.clear()
        self.label_3.setText("")

    def showOnePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showTwoPage(self):
        self.stackedWidget.setCurrentIndex(1)

    def read_file(self, file_name):
        file_handle = open(file_name, 'r')  # , encoding='ANSI'
        text = file_handle.read().splitlines()  # 读取后以行进行分割
        file_handle.close()
        return text

    def showWebWindow(self, url):
        self.tick_win = SecondWindow()
        self.tick_win.browser = QWebEngineView()
        font = QtGui.QFont()
        font.setFamily("Arial")  # 括号里可以设置成自己想要的其它字体
        font.setPointSize(1)  # 括号里的数字可以设置成自己想要的字体大小
        self.tick_win.browser.setFont(font)
        self.tick_win.browser.load(QUrl(url))

        self.tick_win.setCentralWidget(self.tick_win.browser)
        self.tick_win.show()

    def compare_file(self):
        if((len(self.list_pre.selectedItems()) == 0) | (len(self.list_post.selectedItems()) == 0)):
            QMessageBox.information(self,"","没有选中需对比的代码文件！",QMessageBox.Yes)
        else:
            file1_name = self.list_pre.selectedItems()[0].whatsThis()
            file2_name = self.list_post.selectedItems()[0].whatsThis()

            text1_lines = self.read_file(file1_name)
            text2_lines = self.read_file(file2_name)
            diff = difflib.HtmlDiff()  # 创建htmldiff对象
            result=diff.make_file(text1_lines, text2_lines)  # 通过make_file方法输出html格式的对比结果#将结果保存到比较结果.html文件中并打开
            try:
                with open('compare_result.html','w') as result_file:  # 同f=open('文本比对结果.html','w')打开或创建一个比对结果.html文件
                    result_file.write(result)  # 同f.write(result)
                    # win32api.MessageBox(0,比对结束，结果存放在当前目录的文本比较结果.html中,程序运行结束,win32con.MB_OK)
            except IOError as error:
                print('写入html文件错误：{0}'.format(error))

            self.showWebWindow("file:///"+self.basedirpath+"/compare_result.html")  # 绝对路径

    def showPDF(self):
        w = QLabel()
        path = self.basedirpath +"/Pyverilog-develop/report.pdf"
        url = bytearray(QUrl.fromLocalFile(path).toEncoded()).decode()
        text = "<a href={}>Reference Link> </a>".format(url)
        w.setText(text)
        w.setOpenExternalLinks(True)
        w.show()

    def showEchart(self,link_matrix, label_list, value_list):
        # 通过 target=函数名 的方式定义子线程
        thread = Thread()
        thread.start()
        # time.sleep(2)  # 隔一秒
        visualize.write_data(link_matrix, label_list, value_list)
        self.showWebWindow("http://localhost:8099/index.html")  # 图形化

    def signalAnalyzePre(self):
        pre = []
        # 获取listwidget中条目数
        count = self.list_pre.count()
        # 遍历listwidget中的内容
        for i in range(count):
            pre.append(self.list_pre.item(i).whatsThis().split("/")[-1])
        # 设置新的工作目录
        os.chdir(self.basedirpath +"/Pyverilog-develop")
        link_matrix, label_list, value_list, listoneregrank = examples.example_parser.use(pre)
        enhanceone.changeindex(listoneregrank,pre)
        ts.rpt(listoneregrank, pre)  # 生成pdf
        self.showPDF()
        os.chdir(self.basedirpath)
        # self.showEchart(link_matrix, label_list, value_list)
        # 关键节点图
        trifinder_event_demo.draw(link_matrix, label_list, value_list)

    def signalAnalyzePost(self):
        post = []
        # 获取listwidget中条目数
        count = self.list_post.count()
        # 遍历listwidget中的内容
        for i in range(count):
            post.append(self.list_post.item(i).whatsThis().split("/")[-1])
        # 设置新的工作目录
        os.chdir(self.basedirpath+"/Pyverilog-develop")
        link_matrix, label_list, value_list, listoneregrank = examples.example_parser.use(post)
        enhanceone.changeindex(listoneregrank,post) 
        ts.rpt(listoneregrank, post)  # 生成pdf
        self.showPDF()
        os.chdir(self.basedirpath)
        # self.showEchart(link_matrix, label_list, value_list)
        # 关键节点图
        trifinder_event_demo.draw(link_matrix, label_list, value_list)

    def signalEnhance(self):
        pre = []
        # 获取listwidget中条目数
        count = self.list_pre.count()
        # 遍历listwidget中的内容
        for i in range(count):
            pre.append(self.list_pre.item(i).whatsThis().split("/")[-1])
        # 设置新的工作目录
        os.chdir(self.basedirpath +"/Pyverilog-develop")
        link_matrix, label_list, value_list, listoneregrank = examples.example_parser.use(pre)
        enhanceone.changeindex(listoneregrank, pre)
        enhanceone.enhanceall(listoneregrank, pre, 1)
        os.chdir(self.basedirpath)

        # self.timer = QBasicTimer()
        # self.timer.start(100, self)
        self.clearPost()
        files = []
        for root, dirs, f in os.walk(self.basedirpath+"/Pyverilog-develop/newverilog/"):
            for i in f:
                files.append(self.basedirpath + "/Pyverilog-develop/newverilog/"+i)

        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document_edit.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])

            if file_name not in self.prelist:
                item.setBackground(QBrush(QColor(200, 200, 255)))

            self.list_post.addItem(item)

        self.list_post.currentItemChanged.connect(self.handlePostChanged)
        self.list_post.itemClicked.connect(self.showPostode)

    def zongxianEnhance(self):
        # 设置新的工作目录
        os.chdir(self.basedirpath + "/python_riscv")
        path1 = self.list_pre.item(0).whatsThis()
        list = path1.split("/")
        filename = list[-1]
        list.pop()
        filepath = os.path.join(*list)
        filepath = "/"+filepath
        print("filename="+filename)
        print("filepath="+filepath)
        enhanceSecurityTop.use(0, filename, filepath)  # 0选项的生成文件在sm3_4decode/ll3 下
        os.chdir(self.basedirpath)

        self.clearPost()
        # listpre = self.list_pre.
        files = []
        for root, dirs, f in os.walk(self.basedirpath + "/python_riscv/sm3_4decode/ll3/"):
            for i in f:
                files.append(self.basedirpath + "/python_riscv/sm3_4decode/ll3/"+i)
        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document_edit.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])

            if file_name not in self.prelist:
                item.setBackground(QBrush(QColor(200, 200, 255)))

            self.list_post.addItem(item)

        self.list_post.currentItemChanged.connect(self.handlePostChanged)
        self.list_post.itemClicked.connect(self.showPostode)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainCode()

    MainWindow.show()
    sys.exit(app.exec_())
