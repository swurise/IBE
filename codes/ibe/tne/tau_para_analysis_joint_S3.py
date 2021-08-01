#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
import math
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
import numpy as np
#-------------AUC-----------------
import random
def auc(myvecfile, dataset):
    node2vec = {}
    f = open(myvecfile, 'rb')
    # print(mypath1)
    # f = open('temp/zhihu_pages_score_merge_stock13.txt', 'rb')    # open函数，发现参数写为‘wb’，即按二进制write
    # f = open('temp/embed.txt', 'rb')    # open函数，发现参数写为‘wb’，即按二进制write
    for i, j in enumerate(f):           # enumerate(sequence, [start=0]), sequence：一个序列、迭代器或其他支持迭代对象,提取节点号i,节点嵌入j
        if j.decode() != '\n':
            node2vec[i] = list(map(float, j.strip().decode().split()))

    # huganglin
    graphtestfile=basepath + '/' + dataset +'/graph_test.txt'
    # print(graphtestfile)
    # graphtestfile=mypath+'/edgelistMergeFile/graph_train.txt'
    with open(graphtestfile, 'rb') as f1:
        edges = [list(map(int, i.strip().decode().split())) for i in f1]
    nodes = list(set([i for j in edges for i in j]))
    # print("nodes:",nodes)
    a = 0
    b = 0
    t1=0
    t2=0
    # tn=0 # 循环次数
    for i, j in edges:
        # tn=tn+1
        if i in node2vec.keys() and j in node2vec.keys():
            dot1 = np.dot(node2vec[i], node2vec[j])             # x.dot(y) 等价于 np.dot(x,y) ———x是m*n 矩阵 ，y是n*m矩阵，则x.dot(y) 得到m*m 矩阵
            random_node = random.sample(nodes, 1)[0]            # random.sample(list,n)随机采样列表list 的指定长度n 的随机样本，但是不会改变列表本身的排序
            while random_node == j or random_node not in node2vec.keys():  # 当random_node == j 时重新采样random_node，直到不相等
                random_node = random.sample(nodes, 1)[0]
            dot2 = np.dot(node2vec[i], node2vec[random_node])
            if dot1 > dot2:         # dot1 是边的两个顶点向量点乘值， dot2 是固定x， 随机选取不等于y的的值与x 做点乘得到的值， 如果dot1 > dot2 则边的x，y顶点更相似
                a += 1
                t1=t1+1
            elif dot1 == dot2:      # 如果dot1 == dot2 则边的x，y顶点与x，other顶点一样相似
                a += 0.5
                t2=t2+1
            b += 1
            # if tn%1000==0:
            #     print("Auc value:",tn,":",float(a) / b)
    # random.sample
    return(float(a) / b)
#/-----------------------------

def save_list_2d(SortedPR,filename):
    # print(SortedPR)
    import os
    if (os.path.exists(filename)):
        os.remove(filename)
        # print('移除文件： ' + filename)
    else:
        os.makedirs(filename[:filename.rfind('/') + 1], exist_ok=True)  # 保存前目录不存在就创建文件夹,exist_ok=True存在不创建

    file2 = open(filename, 'w')
    lenspr = len(SortedPR)
    for i in range(len(SortedPR)):
        for j in range(len(SortedPR[i])):
            file2.write(str(SortedPR[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
            file2.write('\t')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    #file2.close()
    if i + 1 != lenspr: file2.write('\n')  # 写完一行立马换行,最后一行不需要换行

def mergeVec_ReturnList(trans0, trans1):
    mergeList=np.c_[trans0,trans1]
    return mergeList

def list_enlargement(list_source, alpha_coefficient):
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j] = float(list_source[i][j]) * int(alpha_coefficient)  # 遍历二维列表做数据转换之用
    return(list_source)

def list_max_int(mydata):
    mypath = basepath + '/' + mydata+ '/topic_matrix'
    L=[]
    for root, dirs, files in os.walk(mypath):
        for file in files:
            mystr=os.path.splitext(file)[0]
            location=int(mystr.find('_'))
            L.append(int(mystr[0:location])) #其中os.path.splitext()函数将路径拆分为文件名+扩展名
    return(max(L))

# 读文件里面的数据转化为二维列表,行空不处理
def read_List(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []

     #------modify by hu 判断维度 默认1，2行是不能为空的，否则报错--------
    column_list = list_row[0].strip().split()
    emb_dimen0 = column_list.__len__()
    # print(column_list)
    if int(emb_dimen0)>0:list_source.append(column_list)
    else:print('emb_dimen0:',emb_dimen0)
    column_list = list_row[1].strip().split()
    emb_dimen1=column_list.__len__()
    list_source.append(column_list)
    #-------------
    for i in range(2,len(list_row)):
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

# 读文件里面的数据转化为二维列表,行空不处理
def read_Mean_List(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []

     #------modify by hu 判断维度 默认1，2行是不能为空的，否则报错--------
    column_list = list_row[0].strip().split()
    emb_dimen0 = column_list.__len__()
    # print(column_list)
    if int(emb_dimen0)>0:list_source.append(column_list)
    else:print('emb_dimen0:',emb_dimen0)
    column_list = list_row[1].strip().split()
    emb_dimen1=column_list.__len__()
    list_source.append(column_list)
    #-------------
    for i in range(2,len(list_row)):
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
            list_source[i][j]=abs(float(list_source[i][j])) #abs
    file1.close()
    # a = np.array(list_source)
    # print(a.shape)
    # print(np.mean(list_source))
    meanvalue = np.mean(list_source)
    return(meanvalue)

if __name__ == "__main__":
    for mydata in datasets:  # 遍历数据集 modify by huganglin 20200131
        for mymethod in methods:
            print(mydata, '--', mymethod)
            if mymethod == 'CANE':
                if mydata =='wiki' or mydata =='citeseer' or mydata =='blogCatalog' or mydata =='cora_feature2708':
                    print('CANE continue:',mydata,'--',mymethod)
                    print('\n')
                    continue
            if mymethod == 'TADW':
                if mydata !='cora_feature2708':
                    print('TADW continue:',mydata,'--',mymethod)
                    print('\n')
                    continue

            t = list_max_int(mydata)
            for cur_t in range(t + 1):
                methodvector_path = basepath + '/' + mydata + '/method_vector/' + mymethod + '_train_sort_noid.txt'
                topicmatrix_path = basepath + '/' + mydata + '/topic_matrix/' + str(cur_t) + '_topicMatrix.txt'
                jointvector_path = basepath + '/' + mydata + '/tau_para_analysis_joint/' + mymethod + '/' + mymethod + '_' + str(cur_t) + '_joint.txt'
                psi = psi_coefficient_dict.get(mydata + '-' + mymethod, 4)
                # psi = psi_coefficient
                print('psi_coefficient:', psi)

                method_list_source = read_List(methodvector_path)
                topic_list_source = read_List(topicmatrix_path)

                mean_b = read_Mean_List(methodvector_path)
                mean_x = read_Mean_List(topicmatrix_path)
                lambda_coefficient = mean_b / mean_x
                print('lambda_coefficient:', lambda_coefficient)

                auc_method=auc(methodvector_path,mydata)
                auc_topic=auc(topicmatrix_path,mydata)
                alpha_coefficient = pow(auc_topic/auc_method,psi)
                print('alpha_coefficient:', alpha_coefficient)

                if lambda_coefficient>1:
                    topic_list_large_lambda = list_enlargement(topic_list_source, lambda_coefficient)
                    if alpha_coefficient > 1:
                        topic_list_large_lambda_alpha = list_enlargement(topic_list_large_lambda, alpha_coefficient)
                        jointlist = mergeVec_ReturnList(topic_list_large_lambda_alpha, method_list_source)
                        print('topic_list_large_lambda_alpha:', 'topic_list_source*', lambda_coefficient,'*',alpha_coefficient)
                    else:
                        alpha_coefficient = 1/alpha_coefficient
                        method_list_large_alpha = list_enlargement(method_list_source, alpha_coefficient)
                        jointlist = mergeVec_ReturnList(topic_list_large_lambda, method_list_large_alpha)
                        print('topic_list_large_lambda, method_list_large_alpha:', 'topic_list_source*', lambda_coefficient,' method_list_source', '*',
                              alpha_coefficient)
                else:
                    lambda_coefficient = 1/lambda_coefficient
                    method_list_large_lambda = list_enlargement(method_list_source, lambda_coefficient)
                    if alpha_coefficient < 1:
                        alpha_coefficient = 1/alpha_coefficient
                        method_list_large_lambda_alpha = list_enlargement(method_list_large_lambda, alpha_coefficient)
                        jointlist = mergeVec_ReturnList(topic_list_source, method_list_large_lambda_alpha)
                        print('method_list_large_lambda_alpha:', 'method_list_source*', lambda_coefficient, '*',
                              alpha_coefficient)
                    else:
                        topic_list_large_alpha = list_enlargement(topic_list_source, alpha_coefficient)
                        jointlist = mergeVec_ReturnList(topic_list_large_alpha, method_list_large_lambda)
                        print('topic_list_large_alpha, method_list_large_lambda:', 'topic_list_source*', alpha_coefficient,' method_list_source', '*',
                              lambda_coefficient)

                save_list_2d(jointlist, jointvector_path)
                print('生成：:', jointvector_path)
                print('\n')