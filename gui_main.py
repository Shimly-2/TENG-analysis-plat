
"""
---------------------------------------------------------------------------------
License (C) Copyright 2013-2017, Node Supply Chain Manager Corporation Limited.
File Name         :    gui_mian.py
Auther            :    Samenmoer
Software Version  :    Python3.6
Email Address     :    1762851054@qq.com
Creat Time        :    2022/2/23
Description       :
---------------------------------------------------------------------------------
Modification History
Data          By           Version       Change Description
=================================================================================
			|hhh		   |V1.2		|
=================================================================================
---------------------------------------------------------------------------------
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib
import pylab as pl
import xlrd
import pywt
import pandas as pd
import pyautogui
import cv2
import os

pl.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
pl.rcParams['axes.unicode_minus'] = False    #用来正常显示负号
matplotlib.rcParams.update({'font.serif': 'cmr10',
                            'mathtext.fontset': 'cm',
                            })

wavefamilies={1:'haar',2: 'db',3: 'sym',4: 'coif',5: 'bior',6: 'rbio',7: 'dmey',8: 'gaus',9: 'mexh',10: 'morl',11: 'cgau',12: 'shan',13: 'fbsp',14: 'cmor'}
wavelist={
    1:{20: 'haar'},
    2:{21: 'db1', 22: 'db2', 23: 'db3', 24: 'db4', 25: 'db5', 26: 'db6', 27: 'db7', 28: 'db8', 29: 'db9', 30: 'db10', 31: 'db11', 32: 'db12', 33: 'db13', 34: 'db14', 35: 'db15', 36: 'db16', 37: 'db17', 38: 'db18', 39: 'db19', 40: 'db20', 41: 'db21', 42: 'db22', 43: 'db23', 44: 'db24', 45: 'db25', 46: 'db26', 47: 'db27', 48: 'db28', 49: 'db29', 50: 'db30', 51: 'db31', 52: 'db32', 53: 'db33', 54: 'db34', 55: 'db35', 56: 'db36', 57: 'db37', 58: 'db38'},
    3:{59: 'sym2', 60: 'sym3', 61: 'sym4', 62: 'sym5', 63: 'sym6', 64: 'sym7', 65: 'sym8', 66: 'sym9', 67: 'sym10', 68: 'sym11', 69: 'sym12', 70: 'sym13', 71: 'sym14', 72: 'sym15', 73: 'sym16', 74: 'sym17', 75: 'sym18', 76: 'sym19', 77: 'sym20'},
    4:{78: 'coif1', 79: 'coif2', 80: 'coif3', 81: 'coif4', 82: 'coif5', 83: 'coif6', 84: 'coif7', 85: 'coif8', 86: 'coif9', 87: 'coif10', 88: 'coif11', 89: 'coif12', 90: 'coif13', 91: 'coif14', 92: 'coif15', 93: 'coif16', 94: 'coif17'},
    5:{95: 'bior1.1', 96: 'bior1.3', 97: 'bior1.5', 98: 'bior2.2', 99: 'bior2.4', 100: 'bior2.6', 101: 'bior2.8', 102: 'bior3.1', 103: 'bior3.3', 104: 'bior3.5', 105: 'bior3.7', 106: 'bior3.9', 107: 'bior4.4', 108: 'bior5.5', 109: 'bior6.8'},
    6:{110: 'rbio1.1', 111: 'rbio1.3', 112: 'rbio1.5', 113: 'rbio2.2', 114: 'rbio2.4', 115: 'rbio2.6', 116: 'rbio2.8', 117: 'rbio3.1', 118: 'rbio3.3', 119: 'rbio3.5', 120: 'rbio3.7', 121: 'rbio3.9', 122: 'rbio4.4', 123: 'rbio5.5', 124: 'rbio6.8'},
    7:{125:'dmey'},
    8:{126: 'gaus1', 127: 'gaus2', 128: 'gaus3', 129: 'gaus4', 130: 'gaus5', 131: 'gaus6', 132: 'gaus7', 133: 'gaus8'},
    9:{134:'mexh'},
    10:{135:'morl'},
    11:{136: 'cgau1', 137: 'cgau2', 138: 'cgau3', 139: 'cgau4', 140: 'cgau5', 141: 'cgau6', 142: 'cgau7', 143: 'cgau8'},
    12:{144:'shan'},
    13:{145:'fbsp'},
    14:{146:'cmor1-1.5',147:'cmor1.5-1',148:'cmor1.5-2',149:'cmor2-1',150:'cmor3-3',151:'cmor4-3',152:'cmor5-2'}
}

class MyDesiger(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyDesiger, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置

        self.wavefamilies=wavefamilies
        self.wavelist=wavelist

        self.comboBox.clear()  # 清空items
        self.comboBox.addItem('请选择')
        for k, v in self.wavefamilies.items():
            self.comboBox.addItem(v, k)  # 键、值反转

        self.pushButton.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_2.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_3.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_4.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_5.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_6.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")
        self.pushButton_7.setStyleSheet(
            "QPushButton{background-color: rgb(220,220,220);border:2px groove gray;border-radius:10px;padding:2px 4px;border-style: outset;}"
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}")

        self.groupBox1 = Figure_Canvas()
        self.groupBoxlayout = QGridLayout(self.groupBox)
        self.groupBoxlayout.addWidget(self.groupBox1)

        self.groupBox2 = Figure_Canvas()
        self.groupBoxlayout2 = QGridLayout(self.groupBox_2)
        self.groupBoxlayout2.addWidget(self.groupBox2)

        self.groupBox3 = Figure_Canvas()
        self.groupBoxlayout3 = QGridLayout(self.groupBox_3)
        self.groupBoxlayout3.addWidget(self.groupBox3)

        self.pushButton.clicked.connect(self.draw_ori)
        self.pushButton_2.clicked.connect(self.draw_wavelit)
        self.pushButton_3.clicked.connect(self.openfile)
        self.pushButton_3.clicked.connect(self.creat_table_show)
        self.pushButton_4.clicked.connect(self.draw_FFT)
        self.pushButton_5.clicked.connect(self.store_ori)
        self.pushButton_6.clicked.connect(self.store_FFT)
        self.pushButton_7.clicked.connect(self.store_wavelit)
        # self.pushButton_8.clicked.connect(self.plot_all)
        self.horizontalSlider.valueChanged.connect(self.valChange)
        self.horizontalSlider_2.valueChanged.connect(self.valChange2)

    def valChange(self):
        self.spinBox_2.setValue(self.horizontalSlider.value())
        self.groupBoxlayout.removeWidget(self.groupBox1)
        # self.t = table.col_values(0, 1)
        # self.data = table.col_values(1, 1)
        self.horizontalSlider.setMaximum(len(self.t))
        self.groupBox1.plot_ori(self.t, self.data)
        self.groupBox1.plot_line(self.horizontalSlider.value()/1000)
        self.groupBox1.plot_line2(self.horizontalSlider_2.value() / 1000)
        self.groupBox1.fig.canvas.draw()
        self.groupBox1.fig.canvas.flush_events()
        self.groupBoxlayout.addWidget(self.groupBox1)

    def valChange2(self):
        self.spinBox.setValue(self.horizontalSlider_2.value())
        self.groupBoxlayout.removeWidget(self.groupBox1)
        # self.t = table.col_values(0, 1)
        # self.data = table.col_values(1, 1)
        self.horizontalSlider_2.setMaximum(len(self.t))
        self.groupBox1.plot_ori(self.t, self.data)
        self.groupBox1.plot_line2(self.horizontalSlider_2.value()/1000)
        self.groupBox1.plot_line(self.horizontalSlider.value() / 1000)
        self.groupBox1.fig.canvas.draw()
        self.groupBox1.fig.canvas.flush_events()
        self.groupBoxlayout.addWidget(self.groupBox1)

    @pyqtSlot(int)
    def on_comboBox_activated(self, index):
        key = self.comboBox.itemData(index)
        self.comboBox_2.clear()  # 清空items
        if key:
            self.comboBox_2.addItem('请选择')
            # 初始化市
            for k, v in self.wavelist[key].items():
                self.comboBox_2.addItem(v, k)  # 键、值反转

    def store_ori(self):
        x, y = pyautogui.locateCenterOnScreen('screenshot1.bmp')  # 如果这么写就表示在当前目录下
        # print(x,y)
        # print(self.groupBox.x(),self.groupBox.y(),self.groupBox.height,self.groupBox.width)
        img=pyautogui.screenshot(region=[x-175-135/2+340+20,y-80-40/2+20+22,self.groupBox.width()-30,self.groupBox.height()-35])
        img=cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                self.cwd,  # 起始路径
                                                                "PNG Files (*.png);;JPG Files (*.jpg)")
        cv2.imwrite(fileName_choose,img)

    def store_FFT(self):
        x, y = pyautogui.locateCenterOnScreen('screenshot3.bmp')  # 如果这么写就表示在当前目录下
        # print(x,y)
        # print(self.groupBox.x(),self.groupBox.y(),self.groupBox.height,self.groupBox.width)
        img = pyautogui.screenshot(
            region=[x - 175- 135/2+ 340 + 20,
                    y - 200-40/2 +420 + 22,
                    self.groupBox3.width() - 30, self.groupBox3.height() ])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                self.cwd,  # 起始路径
                                                                "PNG Files (*.png);;JPG Files (*.jpg)")
        cv2.imwrite(fileName_choose, img)

    def store_wavelit(self):
        x, y = pyautogui.locateCenterOnScreen('screenshot2.bmp')  # 如果这么写就表示在当前目录下
        # print(x,y)
        # print(self.groupBox.x(),self.groupBox.y(),self.groupBox.height,self.groupBox.width)
        img = pyautogui.screenshot(
            region=[x - 175-135/2 + 980 + 20,
                    y - 140 - 40/2 + 420 + 22,
                    self.groupBox2.width() - 30, self.groupBox2.height()])
        img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,
                                                                "文件保存",
                                                                self.cwd,  # 起始路径
                                                                "PNG Files (*.png);;JPG Files (*.jpg)")
        cv2.imwrite(fileName_choose, img)

    def openfile(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        global path_openfile_name,table
        # print(openfile_name)
        path_openfile_name = openfile_name[0]
        xl = xlrd.open_workbook(openfile_name[0])
        table = xl.sheet_by_index(0)

    def creat_table_show(self):
        if len(path_openfile_name) > 0:
            input_table = pd.read_excel(path_openfile_name)
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            input_table_header = input_table.columns.values.tolist()

            self.tableWidget.setColumnCount(input_table_colunms)
            self.tableWidget.setRowCount(input_table_rows)
            self.tableWidget.setHorizontalHeaderLabels(input_table_header)

            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]
                # print(input_table_rows_values)
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                # print(input_table_rows_values_list)
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]

                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget.setItem(i, j, newItem)

            self.t = table.col_values(0, 1)
            self.data = table.col_values(1, 1)
            self.groupBox1.plot_ori(self.t, self.data)

    def plot_all(self,x):
        t = table.col_values(0, 1)
        data = table.col_values(1, 1)
        self.groupBox1.plot_ori(t, data)
        # self.groupBox1.plot_line(x/1000)

    # def draw_all(self):
    #     self.plot_all(self.horizontalSlider.value())

    def draw_ori(self):
        # xl = xlrd.open_workbook(r'C:/Users/17628/Desktop/for_tyre/1.xlsx')
        # table = xl.sheet_by_index(0)
        t1 = table.col_values(0, self.spinBox.value(), self.spinBox_2.value())
        data1 = table.col_values(1, self.spinBox.value(), self.spinBox_2.value())
        # print(self.groupBox1.plt.ylim())
        # t2=[]
        # m=0
        # for i in range(self.spinBox.value(), self.spinBox_2.value()):
        #     t2[m]=t1[i]
        #     m=m+1
        # data2 = []
        # m = 0
        # for i in range(self.spinBox.value(), self.spinBox_2.value()):
        #     data2[m] = data1[i]
        #     m = m + 1
        # self.t=t2
        # self.data=data2

        self.groupBoxlayout.removeWidget(self.groupBox1)
        self.groupBox1.plot_ori(t1, data1)
        self.groupBox1.fig.canvas.draw()
        self.groupBox1.fig.canvas.flush_events()
        self.groupBoxlayout.addWidget(self.groupBox1)

    def draw_wavelit(self):
        # xl = xlrd.open_workbook(r'C:/Users/17628/Desktop/for_tyre/1.xlsx')
        # table = xl.sheet_by_index(0)
        t = table.col_values(0, self.spinBox.value(), self.spinBox_2.value())
        data = table.col_values(1, self.spinBox.value(), self.spinBox_2.value())

        sampling_rate = 256
        wavename=self.comboBox_2.currentText()
        print(wavename)
        # wavename = 'cmor3-3'
        totalscal = 256
        fc = pywt.central_frequency(wavename)
        cparam = 2 * fc * totalscal
        scales = cparam / np.arange(totalscal, 1, -1)
        [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)

        self.groupBoxlayout2.removeWidget(self.groupBox2)
        self.groupBox2.plot_wavelit(t, frequencies, cwtmatr)
        self.groupBox2.fig.canvas.draw()
        self.groupBox2.fig.canvas.flush_events()
        self.groupBoxlayout2.addWidget(self.groupBox2)

    def draw_FFT(self):
        # xl = xlrd.open_workbook(r'C:/Users/17628/Desktop/for_tyre/1.xlsx')
        # table = xl.sheet_by_index(0)
        t = table.col_values(0, self.spinBox.value(), self.spinBox_2.value())
        data = table.col_values(1, self.spinBox.value(), self.spinBox_2.value())

        self.groupBoxlayout3.removeWidget(self.groupBox3)
        self.groupBox3.plot_FFT(data)
        self.groupBox3.fig.canvas.draw()
        self.groupBox3.fig.canvas.flush_events()
        self.groupBoxlayout3.addWidget(self.groupBox3)


class Figure_Canvas(FigureCanvas):
    def __init__(self, width=3.2, height=2.7):
        self.fig = Figure(figsize=(width, height), dpi=70)
        super(Figure_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)  # 111表示1行1列，第一张曲线图

    # 绘制原始音频信号
    def plot_ori(self, x, y):
        self.ax.cla()  # 清除绘图区
        self.ax.set_xlabel('时间/s')  # 设置坐标名称
        self.ax.set_ylabel('幅度')
        self.ax.set_title('原始音频信号')
        self.ax.plot(x, y)
        self.min=self.ax.set_ylim()[0]
        self.max=self.ax.set_ylim()[1]
        # print(self.ax.set_ylim()[0])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # 绘制原始音频信号
    def plot_wavelit(self, t, frequencies, cwtmatr):
        self.ax.cla()  # 清除绘图区
        self.ax.set_xlabel('时间/s')  # 设置坐标名称
        self.ax.set_ylabel('幅度')
        self.ax.set_title('原始音频信号')
        self.ax.contourf(t, frequencies, abs(cwtmatr))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # 绘制原音频信号的FFT
    def plot_FFT(self, y):
        f1, absY1 = FFT(y)
        self.ax.cla()  # 清除绘图区
        self.ax.set_xlabel('点数')  # 设置坐标名称
        self.ax.set_ylabel('幅度')
        self.ax.set_title('原音频信号的FFT')
        self.ax.plot(f1, absY1)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    # 绘制原音频信号的FFT
    def plot_line(self, x):
        # self.ax.cla()  # 清除绘图区
        self.ax.plot([x,x], [self.min, self.max],'g')
        self.fig.canvas.draw()

    def plot_line2(self, x):
        # self.ax.cla()  # 清除绘图区
        self.ax.plot([x, x], [self.min, self.max], 'r')
        self.fig.canvas.draw()
        # self.fig.canvas.flush_events()

def FFT(y1):
    N1 = len(y1)  # 采样点数
    fs = 10000.0  # 采样频率
    df1 = fs / (N1 - 1)  # 分辨率
    f1 = [df1 * n for n in range(0, N1)]  # 构建频率数组
    Y1 = np.fft.fft(y1) * 2 / N1  # *2/N 反映了FFT变换的结果与实际信号幅值之间的关系
    absY1 = [np.abs(x) for x in Y1]  # 求傅里叶变换结果的模
    return f1, absY1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MyDesiger()
    ui.show()
    sys.exit(app.exec_())