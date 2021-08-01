'''
https://www.bilibili.com/video/av67331139/?p=2 神经网络讲解超好
数据是管理的依据和基础，也是挖掘算法的基础，用事实说话，事实与结果有直接因果关系，事实是自由行为模式下的轨迹，也就是自由行为模式的采样
中西方对自由的理解不同，西方是制度下的自由，也就是制定制度是在制度的约束下，中国是自由下的制度，制定制定是想当然地制定制度，也就是说中国的自由度更大，可以突破制度
'''
import random
# import os
import numpy as np
node2vec = {}
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
def auc(myvecfile, dataset):
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
    print("Auc value:", float(a) / b)

def list_alltopicfile(mydata):
    mypath = basepath + '/'+mydata+'/topic_matrix'
    # print(mypath)
    L=[]
    li_temp = []
    for root, dirs, files in os.walk(mypath):
        for file in files:
            mystr=os.path.splitext(file)[0]
            location=int(mystr.find('_'))
            L.append(int(mystr[0:location])) #其中os.path.splitext()函数将路径拆分为文件名+扩展名
        li_temp.append(mypath + '/' + str(max(L))+ '_topicMatrix.txt')
    return li_temp


def list_byjointfile(mydata):
    mypath = basepath + '/' + mydata + '/joint_vector'
    # print(mypath)
    li_name = []
    li_temp = []
    for root, dirs, files in os.walk(mypath):
        print('files',files)
        for file in files:
            mystr=os.path.splitext(file)[0]
            li_temp = mystr.split('_')
            # list_name = int(mystr.find('_'))

            # print(mypath + '/' + mystr + '.txt')
            li_name.append(mypath + '/' + mystr + '.txt') #其中os.path.splitext()函数将路径拆分为文件名+扩展名

            # print(basepath + '/' + mydata + '/method_vector/' + li_temp[0] + '_train_sort_noid.txt')
            li_name.append(basepath + '/' + mydata + '/method_vector/' + li_temp[0] + '_train_sort_noid.txt')

            # print(basepath + '/' + mydata + '/topic_matrix/' + li_temp[1] + '_topicMatrix.txt')
            li_name.append(basepath + '/' + mydata + '/topic_matrix/' + li_temp[1] + '_topicMatrix.txt')

        return(li_name)

if __name__ == "__main__":
    # for mydata in datasets:  # 遍历数据集 modify by huganglin 20200131
        mydata='wiki'
        file = list_byjointfile(mydata)
        # print(mydata)
        # file = list_alltopicfile(mydata)
        # print(file)
        for f in file:
            print(f)
            auc(f, mydata)

'''
str.decode(encoding='UTF-8',errors='strict')， 以encoding 指定的编码格式解码字符串， 默认编码为字符串编码， 返回解码后的字符串
strip 可以删除字符串的某些字符，而split则是根据规定的字符将字符串进行分割。s.strip(rm)，s为字符串，rm为要删除的字符序列
map() 返回的是迭代器，不是我们直接想要的list
map( func, seq1[, seq2...] ) 函数是将func作用于seq中的每一个元素(list)，并用一个列表给出返回值。如果func为None，作用同zip()。map可以把一个 list 转换为另一个 list，只需要传入转换函数
'''

'''
{字典}, (元祖), [列表list]
os.path.join(path1[,path2[,path3[,...[,pathN]]]]) 将多个路径组合后返回。 'sep'.join(seq) 返回一个以分隔符sep连接各个元素后生成的新字符串
'''
'''
中国人民通过对 ASCII 编码的中文扩充改造，产生了 GB2312 编码，可以表示6000多个常用汉字。
汉字实在是太多了，包括繁体和各种字符，于是产生了 GBK 编码，它包括了 GB2312 中的编码，同时扩充了很多。
中国是个多民族国家，各个民族几乎都有自己独立的语言系统，为了表示那些字符，继续把 GBK 编码扩充为 GB18030 编码。
每个国家都像中国一样，把自己的语言编码，于是出现了各种各样的编码，如果你不安装相应的编码，就无法解释相应编码想表达的内容。
终于，有个叫 ISO 的组织看不下去了。他们一起创造了一种编码 UNICODE ，这种编码非常大，大到可以容纳世界上任何一个文字和标志。所以只要电脑上有 UNICODE 这种编码系统，无论是全球哪种文字，只需要保存文件的时候，保存成 UNICODE 编码就可以被其他电脑正常解释。
UNICODE 在网络传输中，出现了两个标准 UTF-8 和 UTF-16，分别每次传输 8个位和 16个位。于是就会有人产生疑问，UTF-8 既然能保存那么多文字、符号，为什么国内还有这么多使用 GBK 等编码的人？因为 UTF-8 等编码体积比较大，占电脑空间比较多，如果面向的使用人群绝大部分都是中国人，用 GBK 等编码也可以。
————————————————
版权声明：本文为CSDN博主「DanielXH-」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/m0_38080253/article/details/78841280
'''

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

作者：blade_he
链接：https://www.jianshu.com/p/43d866f9c4cf
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''
