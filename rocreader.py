import os
import csv
import chardet
# 首先要把roc文件转成txt
import numpy as np


def roc2txt():
    filepath = './Data/normal/'
    files = os.listdir(filepath)
    for file in files:
        if file.endswith('.roc'):
            newname = file.replace('.roc', '.txt')
            os.renames(filepath + file, filepath + newname)
    print("Done")


def lr2onehot(file, lr):
    onehot = np.zeros(20)
    try:
        onehot[int(lr)-1] = 1
    except:
        print(file, "岩性异常")
    return onehot

# 然后要把转好的txt读进来
def txt2list():
    filepath = './Data/normal/'
    files = os.listdir(filepath)
    with open('lr.csv', 'w', encoding='UTF8', newline='') as lr:
        writer = csv.writer(lr)
        for file in files:
            with open(filepath + file, 'r') as f:
                # print(file)
                txt = f.readlines()
                line_num = 1
                for line in txt:
                    if 2001 < line_num < 5002:
                        linestr = line.split()
                        # linestr.extend(lr2onehot(file, linestr[1]))
                        writer.writerow(linestr)
                    line_num += 1


# roc2txt()
txt2list()
