# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui',
# licensing of 'mainwindow.ui' applies.
#
# Created: Fri Aug  7 14:55:13 2020
#      by: pyside2-uic  running on PySide2 5.11.4a1.dev1546291887
#
# WARNING! All changes made in this file will be lost!

import sys
import os
import numpy as np
import csv
from PIL import Image, ImageDraw
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea, QLabel
from PyQt5.QtCore import QFile, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QPen

colors = [[0.76590096, 0.0266074, 0.9806378],
           [0.54197179, 0.81682527, 0.95081629],
           [0.0799733, 0.79737015, 0.15173816],
           [0.93240442, 0.8993321, 0.09901344],
           [0.73130136, 0.05366301, 0.98405681],
           [0.01664966, 0.16387004, 0.94158259],
           [0.54197179, 0.81682527, 0.45081629],
           # [0.92074915, 0.09919099 ,0.97590748],
           [0.83445145, 0.97921679, 0.12250426],
           [0.7300924, 0.23253621, 0.29764521],
           [0.3856775, 0.94859286, 0.9910683],  # 10
           [0.45762137, 0.03766411, 0.98755338],
           [0.99496697, 0.09113071, 0.83322314],
           [0.96478873, 0.0233309, 0.13149931],
           [0.33240442, 0.9993321 , 0.59901344],
           [0.77690519,0.81783954,0.56220024],
           # [0.93240442, 0.8993321, 0.09901344],
           [0.95815068, 0.88436046, 0.55782268],
           [0.03728425, 0.0618827, 0.88641827],
           [0.05281129, 0.89572238, 0.08913828],

           ]

 #重定义label
class MyLabel(QLabel):
      #鼠标点击事件
    def __init__(self):
        super(QLabel, self).__init__()
        self.x = []
        self.y = []
        self.sortedx = []
        self.sortedy = []
        self.press = True
    def mousePressEvent(self,event):
        if self.press:
            self.x.append(event.pos().x())
            self.y.append(event.pos().y())
            self.sortedx.append(event.pos().x())
            self.sortedy.append(event.pos().y())
            if len(self.sortedx) % 4 == 0:
                self.SpinalSort()
            self.update()

      #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.press:
            painter = QtGui.QPainter(self)
            # Point = QtCore.QPoint(1,1)
            for i in range(len(self.sortedx)):
                #颜色索引
                ind = (i//4) % 8 + 7
                painter.setPen(QPen(QtCore.Qt.GlobalColor(ind),2,Qt.SolidLine))
                painter.drawEllipse(self.sortedx[i], self.sortedy[i], 2, 2)
                # print(self.sortedx[i], self.sortedy[i])
                # painter.drawEllipse(self.x[i], self.y[i], 2, 2)
                if( i % 4 == 3):
                    centerX = sum(self.sortedx[i-3:i+1])/4
                    centerY = sum(self.sortedy[i-3:i+1])/4
                    painter.setFont(QtGui.QFont('arial', 20))  #给画家设置字体、大小
                    painter.drawText(centerX,centerY,str(i//4 + 1))
                    # print(len(self.x))
                    
    # 鼠标移进时调用
    def enterEvent(self, event):
        self.setCursor(Qt.CrossCursor)  #设置鼠标形状为十字形

        
    #对脊椎从上至下排序：
    def SpinalSort(self):
        curtotalnum = len(self.x)//4
        #根据脊椎中心点y坐标排序
        centerY = np.zeros(curtotalnum)
        for i in range(curtotalnum):
            centerY[i] = sum(self.y[4*i:4*i+4])/4
        ind = np.argsort(centerY)
        NewInd = np.zeros(len(self.x))
        for i in range(curtotalnum*4):
            # NewInd[4*i] = 4*ind[i]
            # NewInd[4*i+1] = 4*ind[i]+1
            # NewInd[4*i+2] = 4*ind[i]+2
            # NewInd[4*i+3] = 4*ind[i]+3
            NewInd[i] =4*ind[i//4]+i%4
        if len(self.x)%4 != 0:
            for i in range(curtotalnum*4,len(self.x)):
                NewInd[i] = i
        NewInd = np.array(NewInd,dtype = "int64")
        x = np.array(self.x)
        y = np.array(self.y)
        self.sortedx = list(x[NewInd])
        self.sortedy = list(y[NewInd])

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width =  self.screenRect.width()
        self.isMarking = False
        self.setupUi(self)
        #脊椎数量
        self.spinenum = 18
        #X光朝向
        self.items = ("正面","侧面","背面")
        self.orientdict = {'正面':'front', "侧面":"lateral", "背面":"back"}
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.width, self.height)
        # 禁止禁止拉伸窗口大小  
        # MainWindow.setFixedSize(self.width, self.height)
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #图片名
        self.ImgName = QtWidgets.QLineEdit(self.centralwidget)
        self.ImgName.setGeometry(QtCore.QRect(self.width*0.33 , self.height*0.01 ,self.width*0.25 , self.height*0.025))
        self.ImgName.setObjectName("ImgName")
        self.ImgName.setReadOnly(1)   #设为只读
        #当前图片号码
        self.ImgNum = QtWidgets.QLabel(self.centralwidget)
        self.ImgNum.setGeometry(QtCore.QRect(self.width*0.88, self.height*0.85, self.height*0.06, self.height*0.04))
        self.ImgNum.setFont(QtGui.QFont("Arial",12))
        self.ImgNum.setObjectName("ImgNum")
        #当前X光朝向
        self.XrayOrient = QtWidgets.QLabel(self.centralwidget)
        self.XrayOrient.setGeometry(QtCore.QRect(self.width*0.88, self.height*0.8, self.height*0.24, self.height*0.04))
        self.XrayOrient.setFont(QtGui.QFont("Arial",12))
        self.XrayOrient.setObjectName("ImgNum")
        #列表框
        self.ImgsList = QtWidgets.QListWidget(self.centralwidget)
        self.ImgsList.setGeometry(QtCore.QRect(self.width*0.005 , self.height*0.044, self.width*0.11 , self.height*0.85))
        self.ImgsList.setObjectName("ImgsList")
        self.ImgsList.doubleClicked.connect(self.ListShow)
        
        #按钮布局
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(self.width*0.88 , self.height*0.046, self.width*0.078 , self.height*0.77))
        self.layoutWidget.setObjectName("layoutWidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        #读取文件夹        
        self.dirButton = QtWidgets.QPushButton(self.layoutWidget)
        self.dirButton.setObjectName("dirButton")
        self.dirButton.clicked.connect(self.select_img_click)     
        self.verticalLayout.addWidget(self.dirButton)
        #读取上一张图片
        self.preButton = QtWidgets.QPushButton(self.layoutWidget)
        self.preButton.setObjectName("preButton")
        self.preButton.setEnabled(False)
        self.preButton.clicked.connect(self.previous_img_click)
        self.verticalLayout.addWidget(self.preButton)
        #读取下一张图片
        self.nextButton = QtWidgets.QPushButton(self.layoutWidget)
        self.nextButton.setObjectName("nextButton")
        self.nextButton.setEnabled(False)
        self.nextButton.clicked.connect(self.next_img_click)
        self.verticalLayout.addWidget(self.nextButton)
        #开始标注
        # self.markButton = QtWidgets.QPushButton(self.layoutWidget)
        # self.markButton.setObjectName("markButton")
        # self.markButton.setEnabled(False)
        # self.markButton.clicked.connect(self.start_marking)
        # self.verticalLayout.addWidget(self.markButton)
        #撤销
        self.UndoButton = QtWidgets.QPushButton(self.layoutWidget)
        self.UndoButton.setObjectName("UndoButton")
        self.UndoButton.setEnabled(False)
        self.UndoButton.clicked.connect(self.Undo)
        self.verticalLayout.addWidget(self.UndoButton)
        #撤销某节脊椎点
        self.CancelButton = QtWidgets.QPushButton(self.layoutWidget)
        self.CancelButton.setObjectName("Cancel")
        self.CancelButton.setEnabled(False)
        self.CancelButton.clicked.connect(self.Cancel)
        self.verticalLayout.addWidget(self.CancelButton)
        #重新标注
        self.remarkButton = QtWidgets.QPushButton(self.layoutWidget)
        self.remarkButton.setObjectName("remarkButton")
        self.remarkButton.setEnabled(False)
        self.remarkButton.clicked.connect(self.remark)
        self.verticalLayout.addWidget(self.remarkButton)
        #保存
        self.saveButton = QtWidgets.QPushButton(self.layoutWidget)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.Save)
        self.verticalLayout.addWidget(self.saveButton)
        #图像展示
        self.ImgShow = MyLabel()
        # self.ImgShow = QtWidgets.QLabel(self.centralwidget)
        # self.ImgShow.setText("")
        self.ImgShow.setObjectName("ImgShow")
        #图像展示滚轮窗口
        self.ImgView = QScrollArea(self.centralwidget)
        self.ImgView.setGeometry(QtCore.QRect(self.width*0.13 , self.height*0.044,  self.width*0.7,  self.height*0.85))
        self.ImgView.setObjectName("ImgView")
        self.ImgView.setWidgetResizable(True)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.width*0.52 , self.height*0.02))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "X光脊椎标注", None, -1))
        self.dirButton.setText(QtWidgets.QApplication.translate("MainWindow", "选择文件夹", None, -1))
        self.preButton.setText(QtWidgets.QApplication.translate("MainWindow", "上一张", None, -1))
        self.nextButton.setText(QtWidgets.QApplication.translate("MainWindow", "下一张", None, -1))
        # self.markButton.setText(QtWidgets.QApplication.translate("MainWindow", "开始标注", None, -1))
        self.UndoButton.setText(QtWidgets.QApplication.translate("MainWindow", "撤销上个点", None, -1))
        self.CancelButton.setText(QtWidgets.QApplication.translate("MainWindow", "撤销某节脊椎点", None, -1))
        self.remarkButton.setText(QtWidgets.QApplication.translate("MainWindow", "重新标注", None, -1))
        self.saveButton.setText(QtWidgets.QApplication.translate("MainWindow", "保存", None, -1))
    
    # 选择目录按钮
    def select_img_click(self):
        try:
            self.ImgsList.clear()
            self.Clear()
            # 得到图片所在文件夹dir_path
            self.dir_path = QtWidgets.QFileDialog.getExistingDirectory(self,'选择文件夹')
            # 存点和带点图片的文件夹
            self.PointsPath = os.path.join(self.dir_path,'points')
            self.ImgWithPointsPath = os.path.join(self.dir_path,'ImgWithPoints')
            
            dir_list = os.listdir(self.dir_path)
            img_list = []
            ## 将图片文件放到列表框中
            for dir in dir_list:
                suffix_list = ['jpg','png','jpeg','bmp']
                if dir.split('.')[-1].lower() in suffix_list:
                    # print(dir)
                    img_list.append(dir)
                    self.ImgsList.addItem(dir)
                        
            if len(img_list) > 0:
                # 图像文件索引字典
                self.totalnum = len(img_list)
                self.img_index_dict = dict()
                self.file_index_dict = dict()
                for i,d in enumerate(img_list):
                    self.img_index_dict[i] = d
                    self.file_index_dict[d] = i
                # print(self.img_index_dict)
                # 查找当前已标记图像并显示为红色
                self.MarkedImg_index_dict = dict()
                if(os.path.exists(self.PointsPath)):
                    marked_list = os.listdir(self.PointsPath)
                    for dir in marked_list:
                        file = os.path.splitext(dir)[0]
                        if file in self.file_index_dict:
                            self.MarkedImg_index_dict[file] = 1
                            self.ImgsList.item(self.file_index_dict.get(file)).setForeground(QColor('red'))
                self.current_index = 0 # 当前的图像索引
                    
                # 当前图片文件路径
                self.current_filename = os.path.join(
                    self.dir_path,self.img_index_dict[self.current_index]
                )
                # 实例化一个图像
                self.Imgshow()

                # 当前文件名
                self.current_text = self.img_index_dict[self.current_index].split('.')[0]
                self.ImgShow.update()
                # 设置ImgNamet控件文本内容
                self.ImgName.setText(self.current_text)

                # 启用其他按钮
                # self.markButton.setEnabled(True)
                self.preButton.setEnabled(True)
                self.nextButton.setEnabled(True)
                self.UndoButton.setEnabled(True)
                self.CancelButton.setEnabled(True)
                self.remarkButton.setEnabled(True)
                self.saveButton.setEnabled(True)

                # 判断当前图片是否已被标注
                self.ismarked()
                # # 设置图片数量信息
                self.ImgNum.setText("{}/{}".format(self.current_index+1,self.totalnum))
                
                
            else:
                QtWidgets.QMessageBox.information(
                    self,'提示','文件夹没有发现图片文件！',
                    QtWidgets.QMessageBox.Ok
                )
        except Exception as e:
            print(repr(e))
    
    # 上一张图片
    def previous_img_click(self):
        # 清空当前点
        self.Clear()        
        # 当前图像索引减1
        self.current_index -= 1
        if self.current_index in self.img_index_dict.keys():
            # 当前图片文件路径
            self.current_filename = os.path.join(
                self.dir_path, self.img_index_dict[self.current_index]
            )
            # 实例化一个图像
            self.Imgshow()
            # 当前文件名
            self.current_text = self.img_index_dict[self.current_index].split('.')[0]
            #判断图片是否已被标注
            self.ismarked()
            # 设置ImgName控件文本内容
            self.ImgName.setText(self.current_text)
            

            # 设置状态栏
            self.ImgNum.setText("{}/{}".format(self.current_index+1,self.totalnum))
        else:
            self.current_index += 1
            QtWidgets.QMessageBox.information(
                self, '提示', '图片列表到顶了！',
                QtWidgets.QMessageBox.Ok
            )
            
    # 下一张图片
    def next_img_click(self):
        # 清空当前点
        self.Clear()
        # 当前图像索引加1
        self.current_index += 1
        if self.current_index in self.img_index_dict.keys():
            # 当前图片文件路径
            self.current_filename = os.path.join(
                self.dir_path, self.img_index_dict[self.current_index]
            )
            # 实例化一个图像
            self.Imgshow()
            # 当前文件名
            self.current_text = self.img_index_dict[self.current_index].split('.')[0]
            # 设置ImgName控件文本内容
            self.ImgName.setText(self.current_text)
            #判断图片是否已被标注
            self.ismarked()


            # 设置状态栏
            self.ImgNum.setText("{}/{}".format(self.current_index+1,self.totalnum))
        else:
            self.current_index -=1
            QtWidgets.QMessageBox.information(
                self,'提示','最后一张图片啦！',
                QtWidgets.QMessageBox.Ok
            )
            
    #点击列表框展示图片
    def ListShow(self):
         self.Clear()  
         index = self.ImgsList.currentRow()
         self.current_index = index
         self.current_filename = os.path.join(
             self.dir_path, self.img_index_dict[self.current_index]
        )
        # 实例化一个图像
         self.Imgshow()
         # 当前文件名
         self.current_text = self.img_index_dict[self.current_index].split('.')[0]
         # 设置ImgName控件文本内容
         self.ImgName.setText(self.current_text)
         #判断图片是否已被标注
         self.ismarked()
         # self.ImgsList.item(index).setForeground(QColor('red'))
         # 设置状态栏
         self.ImgNum.setText("{}/{}".format(self.current_index+1,self.totalnum))
         
    # #开始标注
    # def start_marking(self):
    #     self.ImgShow.press = True
    
    #撤销某节脊椎点
    def Cancel(self):
        num, ok = QtWidgets.QInputDialog.getInt(self, '输入数字', '脊椎号码', 1, 1)
        if ok:
            if 0 < num <= len(self.ImgShow.x)//4:
                num -= 1
                if len(self.ImgShow.x) % 4 == 0:
                    for i in range(0,len(self.ImgShow.x),4):
                        if self.ImgShow.x[i]==self.ImgShow.sortedx[4*num] and self.ImgShow.y[i]==self.ImgShow.sortedy[4*num]:
                            self.ImgShow.x = list(self.ImgShow.x[:i]+self.ImgShow.x[i+4:]) 
                            self.ImgShow.y = list(self.ImgShow.y[:i]+self.ImgShow.y[i+4:])
                            break
                    # self.ImgShow.sortedx = list(self.ImgShow.sortedx[:4*num]+self.ImgShow.sortedx[4*num+4:])
                    # self.ImgShow.sortedy = list(self.ImgShow.sortedy[:4*num]+self.ImgShow.sortedy[4*num+4:])
                    self.ImgShow.SpinalSort()
                    self.ImgShow.update()
                    
                        
                else:
                    QtWidgets.QMessageBox.information(
                    self,'提示','请将当前脊椎4个点都标完！',
                    QtWidgets.QMessageBox.Ok
                )
            
            else:
                QtWidgets.QMessageBox.information(
                    self,'提示','输入号码有误！',
                    QtWidgets.QMessageBox.Ok
                )
            
        
        
    #撤销上一个点
    def Undo(self):
        if len(self.ImgShow.x)>0:
            self.ImgShow.x.pop()
            self.ImgShow.y.pop()
            self.ImgShow.SpinalSort()
            self.ImgShow.update()
        else:
            QtWidgets.QMessageBox.information(
                self,'提示','没有点了！',
                QtWidgets.QMessageBox.Ok
            )
            
    
    #重新标注
    def remark(self):
        
        self.Clear()
    
    #保存
    def Save(self):
        if len(self.ImgShow.x) == self.spinenum * 4 :
            #判断X光图片朝向
            self.item, self.Orient_Pressed = QtWidgets.QInputDialog.getItem(self, "选择X光朝向","当前X光朝向:", self.items, 0, False)
            if self.Orient_Pressed == True:
                self.XrayOrient.setText("当前X光朝向为:{}".format(self.item))
                self.XrayOrient.setVisible(True)
            
                # 在图片所在文件夹下分别建立PointsPath和ImgWithPointsPath文件夹存储点和标有点的图片
                if not os.path.exists(self.PointsPath):
                    os.makedirs(self.PointsPath)
                if not os.path.exists(self.ImgWithPointsPath):
                    os.makedirs(self.ImgWithPointsPath)
                #存点为csv文件
                filename = os.path.join(self.PointsPath,self.img_index_dict[self.current_index]+'.csv')
                with open(filename, "w", encoding = 'utf8',newline = "") as csvFile :#创建csv文件
                    writer = csv.writer(csvFile) #创建写的对象
                    writer.writerow([self.orientdict[self.item]])
                    for i in range(len(self.ImgShow.sortedx)):
                        writer.writerow([self.ImgShow.sortedx[i], self.ImgShow.sortedy[i]])
                #存标点的图片
                image= Image.open(self.current_filename)
                draw = ImageDraw.Draw(image)
                for i in range(len(self.ImgShow.x)):
                    j = i//4
                    color = colors[j]
                    color_255 = (int(255 * color[0]), int(255 * color[1]), int(255 * color[2]))
                    draw.ellipse((self.ImgShow.sortedx[i]-2,self.ImgShow.sortedy[i]-2,self.ImgShow.sortedx[i]+2,self.ImgShow.sortedy[i]+2),fill =color_255)  
                imgname = os.path.join(self.ImgWithPointsPath,self.img_index_dict[self.current_index]+'.png')
    
                image.save(imgname)
                self.MarkedImg_index_dict[self.img_index_dict[self.current_index]] = 1
                self.ImgsList.item(self.current_index).setForeground(QColor('red'))
                QtWidgets.QMessageBox.information(
                    self,'提示','保存成功！',
                    QtWidgets.QMessageBox.Ok
                )
        else:
            QtWidgets.QMessageBox.information(
                self,'提示','需要标注{}节脊椎共{}个点！'.format( self.spinenum, self.spinenum*4 ),
                QtWidgets.QMessageBox.Ok
            )
            
        
    
    #图片展示
    def Imgshow(self):
        # self.image = QtGui.QImage(self.current_filename)
        image = Image.open(self.current_filename)
        self.Qimg = image.toqimage()
        self.QPixmapImg = QtGui.QPixmap.fromImage(self.Qimg)
        # print(self.current_filename)
        # self.img_width = image.width() # 图片宽度
        # self.img_height = image.height() # 图片高度
        # self.img_scale = 1
        # self.image = image.scaled(self.ImgShowWidth,self.ImgShowHeight)
        # 在ImgShow控件中显示图像
        self.ImgShow.setPixmap(self.QPixmapImg)
        self.ImgShow.setAlignment(Qt.AlignLeft)
        self.ImgShow.setAlignment(Qt.AlignTop)


        self.ImgView.setWidget(self.ImgShow)
            
    #清空点
    def Clear(self):
        self.ImgShow.x.clear()
        self.ImgShow.y.clear()
        self.ImgShow.sortedx.clear()
        self.ImgShow.sortedy.clear()
        self.ImgShow.update()
    
    #判断图片是否已标注
    def ismarked(self):
        if self.img_index_dict[self.current_index] in self.MarkedImg_index_dict:   
            filename = os.path.join(self.PointsPath,self.img_index_dict[self.current_index]+'.csv')
            with open(filename, 'r') as f:
                reader = csv.reader(f)
                for i,row in enumerate(reader):
                    if i==0:
                        self.item = row[0]
                    else:
                        self.ImgShow.x.append(int(row[0]))
                        self.ImgShow.sortedx.append(int(row[0]))
                        self.ImgShow.y.append(int(row[1]))
                        self.ImgShow.sortedy.append(int(row[1]))
            orient_ENG2CN = {'front':'正面','lateral':'侧面','back':'背面'}
            self.XrayOrient.setText("当前X光朝向为:{}".format(orient_ENG2CN[self.item]))
            self.XrayOrient.setVisible(True)
            self.ImgShow.press = True
            self.ImgShow.update()
        else:
            self.XrayOrient.setVisible(False)
        

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())