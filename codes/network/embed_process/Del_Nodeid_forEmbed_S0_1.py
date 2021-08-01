#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################

# 读文件里面的数据转化为二维列表
def Read_list_noid(filename):
    file1 = open(filename, "r")
    list_row = file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表， strip()和split() 参数默认是空,\t,\n
        list_source.append(column_list)  # 在末尾追加到list_source

    # 每个元素转换为整型，方便排序
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            # print(len(list_source[i]))
            if j==0:
                list_source[i][0] = ''  # 去掉节点号 #int(list_source[i][0])  # 遍历每行0列元素转换为整数
            else:
                list_source[i][j] = float(list_source[i][j])  # 遍历每行每列元素转换为整数，除了0列
    file1.close()
    # print(list_source)
    return list_source


# 保存二维列表到文件
import os
def Save_list(mergeList, filename):
    if (os.path.exists(filename)):
        os.remove(filename)
        print('移除文件： ' + filename)

    file2 = open(filename, 'w')
    for i in range(len(mergeList)):
        lenLi=len(mergeList[i])
        # print('lenLi:',lenLi)
        if lenLi<2:continue  # 为空不存储
        else:
            for j in range(lenLi):
                file2.write(str(mergeList[i][j]).strip() + ' ')              # write函数不能写int类型的参数，所以使用str()转化
                #file2.write(' ')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    file2.close()

if __name__ == "__main__":
    vecpath=mypath+"/method_vec"
    file_vector_sort =      vecpath+"/"+method+"_train_sort.txt"
    file_vector_sort_noid = vecpath+"/"+method+"_train_sort_noid.txt"
    print(file_vector_sort, ', ', file_vector_sort_noid)
    sorted_noid = Read_list_noid(file_vector_sort)
    Save_list(sorted_noid, file_vector_sort_noid)