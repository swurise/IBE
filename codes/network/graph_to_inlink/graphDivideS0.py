# 把graph划分成训练集和测试集
import random
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
# 修改处1/4
batch_size = 64
ratio= 0.95

f = open(mypath+'/graph.txt', 'rb')
edges = [i for i in f]

selected = int(len(edges) * float(ratio))
print('selected1:',selected,'selected % config.batch_size:',selected % batch_size)
selected = selected - selected % batch_size
print('selected2:',selected)
selected = random.sample(edges, selected)
remain = [i for i in edges if i not in selected]

filename=mypath+'/edgelistMergeFile/graph_train.txt'
os.makedirs(filename[:filename.rfind('/') + 1], exist_ok=True)  # 保存前目录不存在就创建文件夹,exist_ok=True存在不创建
fw1 = open(filename, 'wb')
# 修改处4/4
fw2 = open(mypath+'/graph_test.txt', 'wb')

for i in selected:
    fw1.write(i)

for j in remain:
    fw2.write(j)

fw1.close()
fw2.close()
