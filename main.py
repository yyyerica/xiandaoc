import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QListWidgetItem
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import untitled2


class MainCode(QMainWindow, untitled2.Ui_MainWindow):  # untitled2.Ui_MainWindow

    def __init__(self):
        QMainWindow.__init__(self)
        untitled2.Ui_MainWindow.__init__(self)  # untitled2.Ui_MainWindow
        self.setupUi(self)
        self.button_loadpre.clicked.connect(self.openPreFile)
        self.button_loadpost.clicked.connect(self.openPostFile)

        self.button_clearpre.clicked.connect(self.clearPre)
        self.button_clearpost.clicked.connect(self.clearPost)

        self.button_onepage.clicked.connect(self.showOnePage)
        self.button_twopage.clicked.connect(self.showTwoPage)

    def openPreFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "Open files", "/")[0]  # tuple
        for i in range(len(files)):
            file_name = files[i].split('/')[-1]
            item = QListWidgetItem()
            item.setIcon(QtGui.QIcon(r'./image/document.png'))
            item.setText(file_name)
            item.setWhatsThis(files[i])
            self.list_pre.addItem(item)

        self.list_pre.currentItemChanged.connect(self.handlePreChanged)
        self.list_pre.itemClicked.connect(self.showPreCode)

    def openPostFile(self):  # 选择文本文件上传
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        files = file_name.getOpenFileNames(self, "Open files", "/")[0]  # tuple
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
        data = ""
        with open(self.list_post.selectedItems()[0].whatsThis(), 'r', encoding='utf-8') as f:
            data += f.read()

        self.label_3.setText(data)

    def clearPre(self):
        self.list_pre.clear()
        self.label.setText("")
        self.label_2.setText("")

    def clearPost(self):
        self.list_post.clear()
        self.label_3.setText("")

    def showOnePage(self):
        self.stackedWidget.setCurrentIndex(0)

    def showTwoPage(self):
        self.stackedWidget.setCurrentIndex(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainCode()

    MainWindow.show()
    sys.exit(app.exec_())
