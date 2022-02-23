# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pywt
from matplotlib.font_manager import FontProperties
import xlrd

plt.rcParams['font.sans-serif'] = ['SimHei']  #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    #用来正常显示负号
# chinese_font = FontProperties(fname='/usr/share/fonts/truetype/wqy/wqy-microhei.ttc')

xl = xlrd.open_workbook(r'C:/Users/17628/Desktop/for_tyre/1.xlsx')
xl.sheet_names()
print("sheets：" + str(xl.sheet_names()))
table = xl.sheet_by_index(0)
col = table.col_values(0,1,10000)
# print(col)

sampling_rate = 256

t=col

data=table.col_values(1,1,10000)
# wavename = 'cgau8'
wavename='cmor3-3'
totalscal = 256
fc = pywt.central_frequency(wavename)
cparam = 2 * fc * totalscal
scales = cparam / np.arange(totalscal, 1, -1)
[cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / sampling_rate)
plt.figure(figsize=(8, 4))
plt.subplot(211)
plt.plot(t, data)
plt.xlabel("时间(秒)")
plt.title("300Hz和200Hz和100Hz的分段波形和时频谱", fontsize=20)
plt.subplot(212)
plt.contourf(t, frequencies, abs(cwtmatr))
plt.ylabel("频率(Hz)")
plt.xlabel("时间(秒)")
plt.subplots_adjust(hspace=0.4)
plt.show()