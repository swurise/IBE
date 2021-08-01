#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
path = basepath + '/zhihu/topic_matrix'
L=[]
for root, dirs, files in os.walk(path):
    for file in files:
        mystr=os.path.splitext(file)[0]
        location=int(mystr.find('_'))
        L.append(int(mystr[0:location])) #其中os.path.splitext()函数将路径拆分为文件名+扩展名
print(max(L))
print(L)