#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
# read file directory
inlink=''
inlinks=''
i=-1 #首节点-1，设为0的前一节点-1
print(mypath+"/edgelist_train_sort_S3.txt")
with open(mypath+"/edgelist_train_sort_S3.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')  #去掉列表中每一个元素的换行符
        # print(line)
        if line != "": #防止读入空行
            nodes=line.split()
            # print(nodes[0].__str__()+ '   ' + nodes[1].__str__()+'  i:'+i.__str__())
            if int(nodes[0])==i: # 同一节点连续
                inlink = inlink + ' ' + nodes[1].__str__()
            else:
                if int(nodes[0]) == (i+1):  # 下一节点
                    inlinks = inlinks+ '\n' + inlink
                    inlink= nodes[0].__str__()+ ' ' + nodes[1].__str__() #下一节点
                    i=i+1
                else:
                    inlinks = inlinks + '\n' + inlink
                    while  int(nodes[0]) > i + 1: # 填补中间空节点
                        inlinks = inlinks + '\n' + (i+1).__str__()+' '+(i+1).__str__()  # i+1为下一节点
                        i = i + 1
                    inlink = nodes[0].__str__() + ' ' + nodes[1].__str__() #填补完中间空节点后下一节点
                    i = i + 1
        else:
            print("空:"+i.__str__())
            # i=i+1
    # print('inlinks: ',inlinks)
    inlinks = inlinks + '\n' + inlink #把读入的最后一行加入inlinks中
print('目录： '+ mypath+"/edgelist_train_inlink_S4.txt")
with open(mypath+"/edgelist_train_inlink_S4.txt", "w") as f:
    f.write(inlinks.strip())