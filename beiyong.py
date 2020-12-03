'''
def openImage(self):  # 选择本地图片上传
    global imgName
    # 这里为了方便别的地方引用图片路径，我们把它设置为全局变量
    imgName, imgType = QFileDialog.getOpenFileName(self.centralwidget, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
    # 弹出一个文件选择框，第一个返回值imgName记录选中的文件路径+文件名，第二个返回值imgType记录文件的类型
    jpg = QtGui.QPixmap(imgName).scaled(self.label_image.width(), self.label_image.height())
    # 通过文件路径获取图片文件，并设置图片长宽为label控件的长宽
    self.label_image.setPixmap(jpg)  # 在label控件上显示选择的图片
    self.label_path.setText(imgName)  # 显示所选图片的本地路径
'''
'''
def openVerilogFileTreeWidget(self):  # 选择文本文件上传
    # filter = "Verilog (*.v);;TXT (*.txt);;PDF (*.pdf)"
    file_name = QFileDialog()
    file_name.setFileMode(QFileDialog.ExistingFiles)
    names = file_name.getOpenFileNames(self, "Open files", "/")[0]  # tuple
    # print(names)
    # self.label_path.setText(str(names))
    for a in names:
        # print(a + '\n')
        root = QTreeWidgetItem(self.desWeight)
        root.setText(0, a.split('/')[-1])
        root.setIcon(0, QtGui.QIcon(r'./image/file.png'))
        self.treeWidget.addTopLevelItem(root)

    self.treeWidget.currentItemChanged.connect(self.handleChanged)
'''