import os
from matplotlib import pyplot as plt
import lasio
import csv

"""该程序用于从.las文件中提取数据并写入csv"""
"""
    密度管参数：
    1Depth 深度 2DevV偏差电压 3Cal井径 4DevI偏差电流 5Ng天然伽马 6Lgg长距离Gamma射线 7Sgg短距离Gamma射线
    8Ps电阻率 9Cond电导率

    声波管参数：
    1Depth深度 2TD2第二次声波时效 3T1第一次声波时效

    组合管参数：
    1Depth深度 2SP自然电位 3ResP 16'正常电阻率 4SPR单点电阻率 5NGamma自然伽马总计数 6Tip（Tilt）倾斜 7Azimuth方位角

    温度管参数：1Depth深度 2Temp温度 3F.Ps液体电阻率
"""

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def MDreader():
    filePath = r'./Data/MD/'
    files = os.listdir(filePath)
    # 用来把所有孔的MD数据的其中一列归到一个csv里
    with open('data-md.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for fileName in files:
            print(fileName)
            las = lasio.read(filePath + fileName)

            Depth = las.data[1:, 0].astype('float32')
            DevV = las.data[1:, 1].astype('float32')
            Cal = las.data[1:, 2].astype('float32')
            DevI = las.data[1:, 3].astype('float32')
            Ng = las.data[1:, 4].astype('float32')
            Lgg = las.data[1:, 5].astype('float32')
            Sgg = las.data[1:, 6].astype('float32')
            Ps = las.data[1:, 7].astype('float32')
            Cond = las.data[1:, 8].astype('float32')
            for i in range(1, len(Depth)):
                if Depth[i] == Depth[i-1]:
                    continue
                if 100 <= Depth[i] < 250:
                    writer.writerow([Depth[i], DevV[i], Cal[i], DevI[i], Ng[i], Lgg[i], Sgg[i], Ps[i], Cond[i]])
                    if Depth[i+1]-Depth[i] > 0.06:
                        writer.writerow([Depth[i]+0.05, DevV[i], Cal[i], DevI[i], Ng[i], Lgg[i], Sgg[i], Ps[i], Cond[i]])
                        print("padding at", Depth[i])
        print("MD done")


def SBreader():

    filePath = r'./Data/SB/'
    files = os.listdir(filePath)
    # 用来把SB数据的其中一列归到一个csv里
    with open('data-sb.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for fileName in files:
            print(fileName)
            las = lasio.read(filePath + fileName)
            Depth = las.data[:, 0].astype('float32')
            TD = las.data[:, 1].astype('float32')
            T1 = las.data[:, 2].astype('float32')
            for i in range(1, len(Depth)):
                if Depth[i] == Depth[i-1]:
                    continue
                if 100 <= Depth[i] < 250:
                    writer.writerow([Depth[i], TD[i], T1[i]])
                    if Depth[i+1]-Depth[i] > 0.06:
                        writer.writerow([Depth[i]+0.05, TD[i], T1[i]])
                        print("padding at", Depth[i])
            writer.writerow(' ')
        print("SB done")

def ZHreader():

    filePath = r'./Data/ZH/'
    files = os.listdir(filePath)
    # 用来把ZH数据的其中一列归到一个csv里
    with open('data-zh.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for fileName in files:
            print(fileName)
            las = lasio.read(filePath + fileName)

            Depth = las.data[2000:5000, 0].astype('float32')
            SP = las.data[2000:5000, 1].astype('float32')
            ResP = las.data[2000:5000, 2].astype('float32')
            SPR = las.data[2000:5000, 3].astype('float32')
            NGamma = las.data[2000:5000, 4].astype('float32')
            Tip = las.data[2000:5000, 5].astype('float32')
            Azimuth = las.data[2000:5000, 6].astype('float32')
            for i in range(1, len(Depth)):
                if Depth[i] == Depth[i-1]:
                    continue
                if 100 <= Depth[i] < 250:
                    writer.writerow([Depth[i], SP[i], ResP[i], SPR[i], NGamma[i], Tip[i], Azimuth[i]])
                    if Depth[i+1]-Depth[i] > 0.06:
                        writer.writerow([Depth[i]+0.05, SP[i], ResP[i], SPR[i], NGamma[i], Tip[i], Azimuth[i]])
            writer.writerow(' ')
        print("ZH done")


MDreader()
# SBreader()
# ZHreader()

#以下是lasio的常用方法
# 以HeadItem的方式显示曲线文件头
# print(las.version)
# # 以CurveItem的方式显示曲线道头
# print(las.curves)
# # 显示曲线道的名称
# print(las.keys())
# # 显示las.data的数据类型
# print(type(las.data))
# # 显示测井数据体的形状
# print(las.data.shape)
# # 显示测井数据道的数据类型
# print(type(las[1]))

# 以下都是画图部分
#fig = plt.figure()
# trackNum = las.data.shape[1]

# for i in np.arange(1, trackNum):
#     ax = fig.add_subplot(1, trackNum - 1, 5)
#     ax.plot(las.data[:, 1],las.index)
#     ax.set_xlabel(las.keys()[i])
#     ax.xaxis.tick_top()
#     ax.invert_yaxis()

"""
draw_index = las.index[4000:6000]

for i in range(1, trackNum):
    ax = fig.add_subplot(1, trackNum - 1, i)
    ax.plot(las.data[4000:6000, i], draw_index)

    ax.set_xlabel(las.keys()[i])
    ax.invert_yaxis()
    plt.xticks([])
    plt.yticks([])

plt.show()
"""
