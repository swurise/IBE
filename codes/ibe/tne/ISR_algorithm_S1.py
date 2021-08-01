import sys, string, math
from math import log
from math import modf
import operator
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
outlink_dict = {}   # 存整数，以每行初第一个元素外的其他元素为key的字典，存储入链接数，别人链接我（我是每行第一个元素）
inlink_dict = {}    # 存元素，以每行第一个元素为字典键值编号words[0]，其余元素为值words[1:] 存入字典inlink_dict中
PRank = {}  # 存小数
Temp_PRank = {}  # 临时存储主题敏感向量
new_PRank = {}  # 存小数
Pages = []   # 存元素，语料的每行第一个元素值列表
SortedPR = []
topic_array = []   #存元素， 将主题词切分后存入列表topic_array

d = 0.85

# 扫描标签分类文件，找出分类标签
def list_Node_Label_Class(filename):
  category=[]
  with open(filename, 'r') as fin:
    while 1:
        l = fin.readline()
        if l == '':
            break
        # modify by huganglin 2020/5/20 #
        vec = l.strip().split()
        for i in vec[1:]:
            if i not in category:category.append(i) #分类标签集合列表
    # categoryCount=len(category)#分类标签集合列表元素个数
    return category

#-------------------合并两个向量-------------------------
import numpy as np
def mergeVec_ReturnList(trans0, trans1):
    mergeList=np.c_[trans0,trans1]
    return mergeList
#/-------------------------------------------------------
#-------------------返回二维列表的第1维-------------------------
def get_list_1th(SortedPR):
    trans=[]
    for i in range(len(SortedPR)):  # 行数
        #for j in range(len(SortedPR[i])):  # 列数
        trans.append(SortedPR[i][1])
    return(trans)
#/-------------------------------------------------------
#---------保存二维列表到文件-----------
def Save_list_2d(SortedPR,filename):
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

#保存二维列表中第二维到文件，节点号不保存，保存节点号的向量值
def Save_list_1d(SortedPR,filename):
    import os
    if (os.path.exists(filename)):
        os.remove(filename)
        print('移除文件： ' + filename)
    else:
        os.makedirs(filename[:filename.rfind('/') + 1], exist_ok=True)  # 保存前目录不存在就创建文件夹,exist_ok=True存在不创建

    # print(SortedPR)
    file2 = open(filename, 'w')
    lenspr=len(SortedPR)
    for i in range(lenspr):
            file2.write(str(SortedPR[i]))              # write函数不能写int类型的参数，所以使用str()转化
            # print('i:'+(i+1).__str__()+'len(SortedPR):'+lenspr.__str__()+(i+1!=lenspr).__str__())
            if i+1!=lenspr:file2.write('\n')   # 写完一行立马换行,最后一行不需要换行
    file2.close()
#/----------------------------------------
def parse_file(inlink, topic):
    input = open(inlink, 'r')
    for line in input.readlines():
        words = []
        # words = string.split(line)
        words = line.split()    # 读入每一行并以列表保存
        inlink_dict[words[0]] = words[1:]    # 以每行第一个元素为字典键值编号words[0]，其余元素为值words[1:] 存入字典inlink_dict中
        Pages.append(words[0])   # 字典inlink_dict的健编号words[0]存入Pages中（其实就是语料的每行第一个元素值）

    # for word in string.split(open(topic, 'r').readline()):   # Attmodule 'string' has no attribute 'split'

    # 将主题词切分后存入列表topic_array print(topic+'文件长度'+topic.length())
    for word in (open(topic, 'r').readline()).split(): topic_array.append(word) #格式如：2 8 18 36 56
    # for word in (open(topic, 'r').readline().strip('[,]')).split(','): topic_array.append(word.strip())  # 格式如：[2, 8, 18, 36, 56]
    # print("topic_array: ",topic_array)

    len_dic = float(len(Pages))  # Pages是语料每行第一个元素值列表，Pages的长度就是语料的行数

    for page in Pages:
        PRank[page] = float(1) / len_dic   #PRank以page为key值，初始化值为:1/(语料行数)，Pages是语料每行第一个元素值列表
        Temp_PRank[page] = PRank[page]


    for page in inlink_dict.keys():  # inlink_dict.keys()是语料的每行第一个元素
        for q in inlink_dict[page]:   # inlink_dict[page] 是语料的key是page的元素，即除了第一个元素以外的其他元素
            # if outlink_dict.has_key(q):     # 'dict' object has no attribute 'has_key' 解决办法
            if q in outlink_dict:    # outlink_dict = {}以每行初第一个元素外的其他元素为key的字典
                outlink_dict[q] += 1
            else:
                outlink_dict[q] = 1
    # print(outlink_dict)

def cal_topic_sensitive_pagerank():
    len_dic = float(len(inlink_dict.keys())) # 语料行数,inlink_dict.keys()是语料的每行第一个元素
    print('len_dic',len_dic)
    exitflag= 1 / (len_dic)
    # print('exitflag:' + exitflag.__str__())
    ite = 0
    loss = 10000
    while (loss > exitflag):
        # print(ite)
        loss = 0
        norm = 0  # 正则化范数
        for page in PRank.keys():    #PRank以page为key值，初始化值为:1/(语料行数)，Pages是语料每行第一个元素值列表
            topic_related_page = 1 if page in topic_array else 0  # 如果当前行第一个元素是主题，page = topic_array，设个标志topic_related_page = 1
            # if topic_related_page == 1:
            #     print(page)
            new_PRank[page] = (float(1 - d)*topic_related_page) / float(len(topic_array))   # d = 0.85 当前节点与主题相关占比重0.25
            # print("new_PRank1: ", new_PRank)
            # print("new_PRank1-2: ",new_PRank[page])
            for q in inlink_dict[page]:  # 以page（行的第一值）为键值的当前行元素（除第一个值以外的元素）
                # 统计Pages节点的出度总数，把Pages的排名得分除以出度总数得到每个出度的超链接的贡献值，然后把当前行每个连接贡献值相加就得到第一个节点的被连接排名得分
                # 别的所有节点链接了当前节点，并且链接节点与主题相关占比重0.85
                new_PRank[page] = new_PRank[page] + (d * float(PRank.get(q)) / float(outlink_dict.get(q))) # outlink_dict.get('WT01-B01-3') = outlink_dict['WT01-B01-3']
            norm = norm + new_PRank[page] * new_PRank[page]  # 正则化范数
        norm = math.sqrt(norm) # 正则化范数
        # print('第'+ite.__str__()+'次norm:'+norm.__str__())
        for page in new_PRank.keys():
            PRank[page] = new_PRank.get(page)/norm # 正则化节点page的重要分数PRank
            loss = loss + math.fabs(PRank[page] - Temp_PRank[page])
            Temp_PRank[page] = PRank[page]
        # print('第' + ite.__str__() + '次loss:' + loss.__str__())
        ite = ite + 1

    # 输出所有值
    '''
    for i in range(50):
        print ("PRank.items()-", i , " : ", PRank.items())    
    '''


def top_rank():
    # SortedPR = sorted(PRank.iteritems(), key=operator.itemgetter(1), reverse=True)   # Python3.5中：iteritems变为items
    # SortedPR = sorted(PRank.items(), key=operator.itemgetter(0), reverse=False)
    SortedPR = sorted(PRank.items(), key = lambda asd:asd[0])
    print(SortedPR)
    # for i in range(len(SortedPR)):
    #     print (i ," : ", SortedPR[i])

def test():
    # 字典转化为二维元组 dict1 = {'3': 0.54444, '66': 0.12344, '4': 0.23242, '9': 0.565221}
    tuple0 = tuple(items for items in PRank.items())  # 字典的每一项转换为二维元组
    # print(dict1, '字典转换为二维元组：             ', tuple0)
    # 二维元组转化为二维列表 tuple1 = (('b',1), ('c',4), ('a',2),('a',1))
    SortedPR = list(list(items) for items in list(tuple0))                     #二维元组转换为二维列表
    # SortedPR = sorted(list1, key=operator.itemgetter(0), reverse=False)
    # print(list1)
    return SortedPR
    # print(tuple0,'二维元组转换为二维列表：',list1)



#===========================
#读文件里面的数据转化为二维列表
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
            list_source[i][j]=(list_source[i][j]) #遍历每行每列元素转换为整数
    file1.close()
    # print(list_source)
    return list_source
#/============================


if __name__ == "__main__":
        # ['affairs1,constellation2,economic3,edu4,ent5,fashion6,game7,home8,house9,lottery10,science11,sports12,stock13']
        for mydata in datasets: #遍历数据集 modify by huganglin 20200131
            #----数据集参数设置-----------
            mypath = basepath +'/'+ mydata
            # print('mypath:'+mypath)
            inlink = mypath + '/edgelist_train_inlink_S4.txt'
            print('inlink:', inlink)
            labelfile = mypath + '/node_labels.txt'
            liZi = list_Node_Label_Class(labelfile)
            print('liZi', liZi)
            #file_joint = mypath + '/topic_matrix/topicMatrix1.txt'  # 合并参数存储路径
            list_joint = [] # 合并参数临时列表
            #/----------------------------
            ii=0
            for i in liZi:  # liZi主题社区
                topicname1=str(i)
                topic = mypath+'/SUBV/subV' + topicname1+'.txt'  #主题集合
                #---------判断文件是否为空----
                size = os.path.getsize(topic)
                if size == 0:
                    print(topic + '主题集合是空的')
                    continue
                else:
                    print(topic + '主题集合可用')
                #/----------------------------
                print("topic:",topic)
                parse_file(inlink, topic)
                cal_topic_sensitive_pagerank()
                # top_rank()
                SortedPR =test()
                # filename1 = "result/cora_embed/cora_topicVector_test.txt" #主题向量测试（要嵌入到旧的嵌入）
                # Save_list(SortedPR, filename1)
                filename1 = mypath + '/topic_vector/topicVec_'+topicname1+'.txt' #主题向量（要嵌入到旧的嵌入）
                tran=get_list_1th(SortedPR)
                Save_list_1d(tran, filename1)
                print(mydata+'的' + topicname1 + '主题敏感向量生成完毕！存于路径：' + mypath + '/topic_vector')

                #----组合topic_matrix-------
                # print(mypath + '/topic_matrix/topicMatrix' + topicname1 +'.txt')
                file_joint = mypath + '/topic_matrix/' + ii.__str__() +'_topicMatrix.txt'
                if ii!=0:
                    ii = ii + 1
                    list_joint = mergeVec_ReturnList(list_joint, tran)
                    Save_list_2d(list_joint, file_joint)
                else:
                    ii=ii+1
                    list_joint = tran
                    Save_list_1d(list_joint, file_joint)
                #/-----------------
            #Save_list(list_joint, file_joint)
            print(mydata+'的主题敏感向量和主题敏感矩阵生成完毕！存于路径：'+ mypath + '/topic_matrix')

'''
编码基本知识
最早的编码是iso8859-1，和ascii编码相似。但为了方便表示各种各样的语言，逐渐出现了很多标准编码，重要的有如下几个。

iso8859-1
属于单字节编码，最多能表示的字符范围是0-255，应用于英文系列。比如，字母a的编码为0x61=97。
很明显，iso8859-1编码表示的字符范围很窄，无法表示中文字符。但是，由于是单字节编码，和计算机最基础的表示单位一致，所以很多时候，仍旧使用iso8859-1编码来表示。而且在很多协议上，默认使用该编码。比如，虽然"中文"两个字不存在iso8859-1编码，以gb2312编码为例，应该是"d6d0 cec4"两个字符，使用iso8859-1编码的时候则将它拆开为4个字节来表示："d6 d0 ce c4"（事实上，在进行存储的时候，也是以字节为单位处理的）。而如果是UTF编码，则是6个字节"e4 b8 ad e6 96 87"。很明显，这种表示方法还需要以另一种编码为基础。

GB2312/GBK

这就是汉子的国标码，专门用来表示汉字，是双字节编码，而英文字母和iso8859-1一致（兼容iso8859-1编码）。其中gbk编码能够用来同时表示繁体字和简体字，而gb2312只能表示简体字，gbk是兼容gb2312编码的。

unicode

这是最统一的编码，可以用来表示所有语言的字符，而且是定长双字节（也有四字节的）编码，包括英文字母在内。所以可以说它是不兼容iso8859-1编码的，也不兼容任何编码。不过，相对于iso8859-1编码来说，uniocode编码只是在前面增加了一个0字节，比如字母a为"00 61"。

需要说明的是，定长编码便于计算机处理（注意GB2312/GBK不是定长编码），而unicode又可以用来表示所有字符，所以在很多软件内部是使用unicode编码来处理的，比如java。

UTF
考虑到unicode编码不兼容iso8859-1编码，而且容易占用更多的空间：因为对于英文字母，unicode也需要两个字节来表示。所以unicode不便于传输和存储。因此而产生了utf编码，utf编码兼容iso8859-1编码，同时也可以用来表示所有语言的字符，不过，utf编码是不定长编码，每一个字符的长度从1-6个字节不等。另外，utf编码自带简单的校验功能。一般来讲，英文字母都是用一个字节表示，而汉字使用三个字节。
注意，虽然说utf是为了使用更少的空间而使用的，但那只是相对于unicode编码来说，如果已经知道是汉字，则使用GB2312/GBK无疑是最节省的。不过另一方面，值得说明的是，虽然utf编码对汉字使用3个字节，但即使对于汉字网页，utf编码也会比unicode编码节省，因为网页中包含了很多的英文字符。
'''