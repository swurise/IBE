#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
# 读文件里面的数据转化为二维列表,行空不处理
def read_List(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []

     #------modify by hu 判断维度 默认1，2行是不能为空的，否则报错--------
    column_list = list_row[0].strip().split()
    emb_dimen0 = column_list.__len__()
    # print(column_list)
    start = 1
    if int(emb_dimen0)>3:
        start = 1
        emb_dimen1 = emb_dimen0
        list_source.append(column_list)

    else:
        start = 2
        print('emb_dimen0:',emb_dimen0)
        column_list = list_row[1].strip().split()
        emb_dimen1=column_list.__len__()
        list_source.append(column_list)
    #-------------
    for i in range(start,len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表
        len_column_list=len(column_list)
        if len_column_list == 0 :
            #-----------行为空的话添加emb_dimen1维长度的0----
            temp = ''
            for i in range(int(emb_dimen1)):  # 减一是为了去掉一维度，因为第一个元素是行号
                temp = temp + '0 '
            #/--------------------
            temp_list = temp.strip().split()
            list_source.append(temp_list);
        else:
            list_source.append(column_list)  # 在末尾追加到list_source
    #/---------------------

    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j] = float(list_source[i][j])
    file1.close()
    return(list_source)

#保存二维列表到文件
def refresh_method_vectorfile(filename):
    mergeList=read_List(filename)
    os.remove(filename)
    if (os.path.exists(filename)):
        print('移除文件： ' + filename)
    file2 = open(filename, 'w')
    for i in range(len(mergeList)):
        for j in range(len(mergeList[i])):
            file2.write(str(mergeList[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
            file2.write('\t')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    file2.close()

if __name__ == "__main__":
    for mydata in datasets:  # 遍历数据集 modify by huganglin 20200131
        for mymethod in methods:  # 遍历数据集 modify by huganglin 20200131
            methodvector_path = basepath + '/' + mydata + '/method_vector/' + mymethod + '_train_sort_noid.txt'
            print(methodvector_path)
            refresh_method_vectorfile(methodvector_path)


