# import os
# p=os.system("sort  result/dataSets/zhihu_graph_merge_S2.txt > result/dataSets/zhihu_graph_sort_S3.txt")
# zhihu_graph_merge_S2-1.txt  zhihu_graph_sort_S3.txt
import operator
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
# 读文件里面的数据转化为二维列表
def Read_list(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表， strip()和split() 参数默认是空,\t,\n
        list_source.append(column_list)                # 在末尾追加到list_source

    #每个元素转换为整型，方便排序
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            # print(len(list_source[i]))
            list_source[i][j]=int(list_source[i][j]) #遍历每行每列元素转换为整数
    file1.close()
    # print(list_source)
    SortedPR = sorted(list_source, key=operator.itemgetter(0), reverse=False)
    return SortedPR

#保存二维列表到文件
import os
def Save_list(SortedPR,filename):
    if (os.path.exists(filename)):
        os.remove(filename)
        print('移除文件： ' + filename)
    with open(filename, 'a+') as file2:
        # file2 = open(filename, 'a+')
        for i in range(len(SortedPR)):
            for j in range(len(SortedPR[i])):
                file2.write(str(SortedPR[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
                file2.write(' ')                          # 相当于Tab一下，换一个单元格
            file2.write('\n')   # 写完一行立马换行
        # file2.write('99999 99999')


if __name__ == "__main__":
    file_merge_S2 = mypath+'/bc_adjlist.txt'
    file_sort_S3 = mypath+'/bc_adjlist_sort.txt'

    print(file_merge_S2,', ',file_sort_S3)
    SortedPR=Read_list(file_merge_S2)
    Save_list(SortedPR, file_sort_S3)




