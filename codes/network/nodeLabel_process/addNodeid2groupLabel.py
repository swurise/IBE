# 因为group.txt文件用行号做节点号，不方便处理，因此需要添加节点号成为：节点号 标签分类号。
import numpy as np
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
# 读文件里面的数据转化为二维列表，,行空不处理
def Read_list(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        # print('column_list:',list_row[i])
        if len(list_row[i].split())>0:
            column_list =  (i.__str__()+' '+list_row[i]).strip().split()  # 添加元素号，每一行split后是一个列表
        else:
            column_list = (i.__str__() + ' ' + '0').strip().split() # 如果一行没有数据填充：“行号 0”
            # column_list = ''  # 如果一行没有数据填充空值
        list_source.append(column_list)            # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        # if len(list_source[i])>1:
            for j in range(len(list_source[i])):  # 列数
                list_source[i][j]=int(list_source[i][j])  # 转换每行每列的元素的数据类型
        # else:
        #     list_source[i][0] = '' # 转换每行每列的元素的数据类型
    file1.close()
    return list_source

#保存二维列表到文件
def Save_list(filename0,filename):
    mergeList=Read_list(filename0) # handle the primary data network_embed.txt flag=0,(filename0, 0)
    file2 = open(filename, 'w')
    for i in range(len(mergeList)):
        lenLi=len(mergeList[i])
        # print('lenLi:',lenLi)
        if lenLi<2:continue  # 为空不存储
        else:
            for j in range(lenLi):
                file2.write(str(mergeList[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
                file2.write(' ')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    file2.close()

if __name__ == "__main__":
    # network_embed.txt ['affairs1,constellation2,economic3,edu4,ent5,fashion6,game7,home8,house9,lottery10,science11,sports12,stock13']
    filename0=mypath+'/group.txt'
    filename = mypath+'/node_labels.txt'
    # path="result/cora_embed/"
    Save_list(filename0,filename)