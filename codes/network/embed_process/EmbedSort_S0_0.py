# 对数据向量进行排序，节点为空的向量补0
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
def Read_list_sort(filename):
    file1 = open(filename, "r")
    list_row = file1.readlines()
    list_source = []
    ###########################################################################
    ######modify by hu 判断维度 默认1，2行是不能为空的，否则报错，#############
    ######modify by hu 第1行有可能是行列号标识要判断去掉，第2行用来计算维度####
    ###########################################################################
    column_list = list_row[0].strip().split()
    emb_dimen0 = column_list.__len__()
    if int(emb_dimen0)>10:list_source.append(column_list)
    else:print(emb_dimen0)
    column_list = list_row[1].strip().split()
    emb_dimen1=column_list.__len__()
    list_source.append(column_list)
    ############################################################################
    for i in range(2,len(list_row)): #0行和1行（行数 维数）记录上面单独处理，从第二行开始，modify by hu 2020-08-31
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表， strip()和split() 参数默认是空,\t,\n
        list_source.append(column_list)  # 在末尾追加到list_source

    # 每个元素转换为整型，方便排序

    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            # print(len(list_source[i]))
            if j==0:
                list_source[i][0] = int(list_source[i][0])  # 遍历每行0列元素转换为整数
            else:
                list_source[i][j] = float(list_source[i][j])  # 遍历每行每列元素转换为整数，除了0列
    file1.close()
    # print(list_source)
    SortedPR = sorted(list_source, key=operator.itemgetter(0), reverse=False)
    return SortedPR, emb_dimen1


# 保存二维列表到文件
import os

def Save_list(SortedPR,emb_dimen1, filename):
    if (os.path.exists(filename)):
        os.remove(filename)
        print('移除文件： ' + filename)
    with open(filename, 'a+') as file2:
        # file2 = open(filename, 'a+')
        ii=0
        #######行为空的话添加emb_dimen1维长度的0####
        temp = ''
        for i in range(int(emb_dimen1)-1): # 减一是为了去掉一维度，因为第一个元素是行号
            temp = temp + '0 '
        ############
        for i in range(len(SortedPR)):
            # print(SortedPR[i][0],' ',ii)
            while SortedPR[i][0]>ii:  #SortedPR[i][0]一行第一个元素是行号
                file2.write(str(ii)+' '+temp) # ii是循环的当前行的循环行号
                file2.write('\n')
                ii += 1
            for j in range(len(SortedPR[i])):
                file2.write(str(SortedPR[i][j]) + ' ')  # write函数不能写int类型的参数，所以使用str()转化
                                                        # + ' '相当于Tab一下，换一个单元格
            file2.write('\n')  # 写完一行立马换行
            ii+=1
        # file2.write('99999 99999')


if __name__ == "__main__":
    vecpath=mypath+"/method_vec"
    file_vector = vecpath+"/"+method+"_train_all.txt"
    file_vector_sort = vecpath+"/"+method+"_train_sort.txt"

    print(file_vector, ', ', file_vector_sort)
    SortedPR,emb_dimen1 = Read_list_sort(file_vector)
    Save_list(SortedPR, emb_dimen1, file_vector_sort)




