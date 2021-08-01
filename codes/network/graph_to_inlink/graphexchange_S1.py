#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################

mergepath=mypath+"/edgelistMergeFile"
filename=mergepath+"/graph_train.txt"
file_exchange=mergepath+"/graph_train_exchange_S1.txt"
if (os.path.exists(file_exchange)):
    os.remove(filename)
    print('移除文件： ' + filename)

p=os.system("awk '{print $2,$1}' "+ filename + " > "+ file_exchange)

# p=os.system("awk '{print $2,$1}' /home/huganglin/myprogram/Network/comm_Algo/OpenNE-master/data/cora/cora_edgelist_train.txt > /home/huganglin/myprogram/Network/comm_Algo/OpenNE-master/data/cora/cora_edgelist_train_exchange_S1.txt")
