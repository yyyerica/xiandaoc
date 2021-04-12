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

    def closeEvent(self, event):
        # reply = QtGui.QMessageBox.question(self, 'Message',
        #                                    'Are you sure to quit?', QtGui.QMessageBox.Yes,
        #                                    QtGui.QMessageBox.No)
        # if reply == QtGui.QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()
        self.destroy()


class MainCode(QMainWindow, untitled2.Ui_MainWindow):  # untitled2.Ui_MainWindow

    def __init__(self):
        QMainWindow.__init__(self)
        untitled2.Ui_MainWindow.__init__(self)  # untitled2.Ui_MainWindow
        self.setupUi(self)
        self.setWindowTitle('开源芯片安全检测及优化工具')

        self.prelist = []  # 只包含文件名,用于对比增强前后有无新的代码，顺序不重要
        self.topmoudlenamepre = ""
        self.topmoudlenamepost = ""
        self.basedirpath = os.getcwd()  # /Users/yunyingye/Desktop/desktop/pyqt

        self.button_loadpre.clicked.connect(self.openPreFile)
        self.button_loadpost.clicked.connect(self.openPostFile)

        self.button_clearpre.clicked.connect(self.clearPre)
        self.button_clearpost.clicked.connect(self.clearPost)

        self.button_onepage.clicked.connect(self.showOnePage)
        self.button_twopage.clicked.connect(self.showTwoPage)

        self.tick_win = None  # 用于compare显示
        self.button_compare.clicked.connect(self.compare_file)

        self.button_signal.clicked.connect(self.signalAnalyzePre)
        self.button_signalpost.clicked.connect(self.signalAnalyzePost)

        self.load_prefile.triggered.connect(self.openPreFile)
        self.load_editfile.triggered.connect(self.openPostFile)
        self.signal_enhance.triggered.connect(self.signalEnhance)
        self.zongxian_enhance.triggered.connect(self.zongxianEnhance)
        self.analyzesignal_pre.triggered.connect(self.signalAnalyzePre)
        self.analyzearith_post.triggered.connect(self.signalAnalyzePost)

        # 隐藏自带垂直滚动条scrollbar
        self.list_pre.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_pre_top.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_post.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_post_top.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.list_pre.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.list_post.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # 设置为同一scrollbar一起滚动
        self.list_pre.setVerticalScrollBar(self.verticalScrollBar)
        self.list_pre_top.setVerticalScrollBar(self.verticalScrollBar)
        self.list_post.setVerticalScrollBar(self.verticalScrollBar_2)
        self.list_post_top.setVerticalScrollBar(self.verticalScrollBar_2)

    def openPreFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "打开文件", self.basedirpath+"/Pyverilog-develop/",
                                           "verilog files(*.v)",
                                              options=QFileDialog.DontUseNativeDialog)[0]  # tuple # 绝对路径 # 用默认的Dialog会自动按文件名对文件列表排序

        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            self.prelist.append(file_name)

        self.refresh_listview(files, self.list_pre, self.list_pre_top)

    def openPostFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "打开文件", self.basedirpath+"/Pyverilog-develop/", "verilog files(*.v)",
                                           options=QFileDialog.DontUseNativeDialog)[0]  # tuple

        self.refresh_listview(files, self.list_post, self.list_post_top)

    def refresh_listview(self, filelist, listview, radiolistview):
        for i in range(len(filelist)):
            file_name = filelist[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document.png'))
            item.setWhatsThis(filelist[i])
            item.setText(file_name)
            item.setSizeHint(QSize(100, 20))

            itemradio = QListWidgetItem()
            itemradio.setSizeHint(QSize(20, 20))
            itemradio.setWhatsThis(str(i))
            # itemradio.setText(str(i))
            # radiolistview.setFocusPolicy(QtCore.Qt.NoFocus)

            if file_name not in self.prelist:
                item.setBackground(QBrush(QColor(200, 200, 255)))
                itemradio.setBackground(QBrush(QColor(200, 200, 255)))

            listview.addItem(item)

            radiolistview.addItem(itemradio)
            # radiolistview.setItemWidget(itemradio, QRadioButton(str(i)))

        listview.currentItemChanged.connect(self.handlelistviewChanged)

        if listview == self.list_pre:
            listview.itemClicked.connect(self.showPreCode)
            radiolistview.itemClicked.connect(self.setTopMoudlepre)
        else:
            listview.itemClicked.connect(self.showPostCode)
            radiolistview.itemClicked.connect(self.setTopMoudlepost)

    def setTopMoudlepre(self):
        if len(self.list_pre_top.selectedItems()) == 0:
            return

        # for items in self.list_pre_top.findChildren(QtWidgets.QRadioButton):
        #     if items.isChecked():
        #         index = int(items.text())
        #         print(index)


        index = int(self.list_pre_top.selectedItems()[0].whatsThis())
        self.topmoudlenamepre = self.list_pre.item(index).whatsThis().split("/")[-1]
        # print(self.topmoudlenamepre)

        pre = []
        # self.prelist = []
        # 遍历listwidget中的内容
        for i in range(self.list_pre.count()):
            pre.append(self.list_pre.item(i).whatsThis())
        pre[0], pre[index] = pre[index], pre[0]
        # print(pre)

        self.list_pre.clear()
        self.list_pre_top.clear()
        self.refresh_listview(pre, self.list_pre, self.list_pre_top)

    def setTopMoudlepost(self):
        if len(self.list_post_top.selectedItems()) == 0:
            return
        index = int(self.list_post_top.selectedItems()[0].whatsThis())
        self.topmoudlenamepost = self.list_post.item(index).whatsThis().split("/")[-1]
        #print(self.topmoudlenamepost)

        post = []
        # 遍历listwidget中的内容
        for i in range(self.list_post.count()):
            post.append(self.list_post.item(i).whatsThis())
        post[0], post[index] = post[index], post[0]
        #print(post)

        self.list_post.clear()
        self.list_post_top.clear()
        self.refresh_listview(post, self.list_post, self.list_post_top)

    def handlelistviewChanged(self, current, previous):
        if current != None:
            current.setIcon(QtGui.QIcon(r'./image/document_show.png'))
        if previous != None:
            previous.setIcon(QtGui.QIcon(r'./image/document.png'))

    def showPreCode(self):
        # print(item.text)
        data = ""
        with open(self.list_pre.selectedItems()[0].whatsThis(), 'r', encoding='utf-8') as f:
            data += f.read()

        self.label.setText(data)
        self.label_2.setText(data)

    def showPostCode(self):
        self.showTwoPage()
        data = ""
        with open(self.list_post.selectedItems()[0].whatsThis(), 'r', encoding='utf-8') as f:
            data += f.read()

        self.label_3.setText(data)

    def clearPre(self):
        self.list_pre.clear()
        self.label_2.setText("")
        self.label.setText("")

        self.prelist.clear()
        self.topmoudlenamepre = ""
        self.list_pre_top.clear()

    def clearPost(self):
        self.list_post.clear()
        self.label_3.setText("")
        self.topmoudlenamepost = ""
        self.list_post_top.clear()

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
        if (len(self.list_pre.selectedItems()) == 0) | (len(self.list_post.selectedItems()) == 0):
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

    def showEchart(self, link_matrix, label_list, value_list):
        # 通过 target=函数名 的方式定义子线程
        thread = Thread()
        thread.start()
        # time.sleep(2)  # 隔一秒
        visualize.write_data(link_matrix, label_list, value_list)
        self.showWebWindow("http://localhost:8099/index.html")  # 图形化

    def signalAnalyzePre(self):
        if self.topmoudlenamepre == "":
            QMessageBox.information(self, "", "未指定顶层文件代码", QMessageBox.Yes)
            return
        pre = []
        # 获取listwidget中条目数
        count = self.list_pre.count()
        # 遍历listwidget中的内容
        for i in range(count):
            pre.append(self.list_pre.item(i).whatsThis())
        # print(pre)
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
        if self.topmoudlenamepost == "":
            QMessageBox.information(self, "", "未指定顶层文件代码", QMessageBox.Yes)
            return
        post = []
        # 获取listwidget中条目数
        count = self.list_post.count()
        # 遍历listwidget中的内容
        for i in range(count):
            post.append(self.list_post.item(i).whatsThis())
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
        if self.topmoudlenamepre == "":
            QMessageBox.information(self, "", "未指定顶层文件代码", QMessageBox.Yes)
            return
        # 清空文件夹
        shutil.rmtree(self.basedirpath+"/Pyverilog-develop/new_verilog/")
        os.mkdir(self.basedirpath+"/Pyverilog-develop/new_verilog/")

        pre = []
        # 获取listwidget中条目数
        count = self.list_pre.count()
        # 遍历listwidget中的内容
        for i in range(count):
            pre.append(self.list_pre.item(i).whatsThis())
        # 设置新的工作目录
        os.chdir(self.basedirpath +"/Pyverilog-develop")
        link_matrix, label_list, value_list, listoneregrank = examples.example_parser.use(pre)
        enhanceone.changeindex(listoneregrank, pre)
        enhanceone.enhanceall(listoneregrank, pre, 0)  # 0是前30%的关键信号
        os.chdir(self.basedirpath)

        self.clearPost()
        files = []
        for root, dirs, f in os.walk(self.basedirpath+"/Pyverilog-develop/new_verilog/"):
            for i in f:
                files.append(self.basedirpath + "/Pyverilog-develop/new_verilog/"+i)

        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document_edit.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])
            if file_name not in self.prelist:
                item.setBackground(QBrush(QColor(200, 200, 255)))

            self.list_post.addItem(item)

            itemradio = QListWidgetItem()
            itemradio.setSizeHint(QSize(20, 20))
            itemradio.setWhatsThis(str(i))
            itemradio.setText(str(i))
            self.list_post_top.addItem(itemradio)

        self.list_post.currentItemChanged.connect(self.handlelistviewChanged)
        self.list_post.itemClicked.connect(self.showPostCode)

        self.list_post_top.itemClicked.connect(self.setTopMoudlepost)

    def zongxianEnhance(self):
        if self.topmoudlenamepre == "":
            QMessageBox.information(self, "", "未指定顶层文件代码", QMessageBox.Yes)
            return
        # 设置新的工作目录
        os.chdir(self.basedirpath + "/python_riscv")
        path1 = self.list_pre.item(0).whatsThis()
        list = path1.split("/")
        filename = list[-1]
        list.pop()
        filepath = os.path.join(*list)
        filepath = "/"+filepath

        filenamelist = ""
        # 获取listwidget中条目数
        count = self.list_pre.count()
        # 遍历listwidget中的内容
        for i in range(count):
            filenamelist += self.list_pre.item(i).whatsThis().split("/")[-1]
            filenamelist += ' '

        enhanceSecurityTop.use(0, 0, filename, filenamelist, filepath)  # 0选项的生成文件在sm3_4decode/ll3 下
        os.chdir(self.basedirpath)

        self.clearPost()
        files = []
        for root, dirs, f in os.walk(self.basedirpath + "/python_riscv/sm3_4decode/ll3/"):
            for i in f:
                # print(i)
                if not i.endswith(".v"):
                    continue
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

            itemradio = QListWidgetItem()
            itemradio.setSizeHint(QSize(20, 20))
            itemradio.setWhatsThis(str(i))
            itemradio.setText(str(i))
            self.list_post_top.addItem(itemradio)

        self.list_post.currentItemChanged.connect(self.handlelistviewChanged)
        self.list_post.itemClicked.connect(self.showPostCode)

        self.list_post_top.itemClicked.connect(self.setTopMoudlepost)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainCode()

    MainWindow.show()
    sys.exit(app.exec_())
