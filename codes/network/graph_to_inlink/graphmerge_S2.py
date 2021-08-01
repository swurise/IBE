# coding:utf-8;
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################
def merge_file():
    infiles = os.listdir(mypath + '/edgelistMergeFile') #待合并文件路径,待合并文件必须放在同一个下级目录里
    print('infiles:' + infiles.__str__())
    outfile = mypath+'/edgelist_train_merge_S2.txt'  #输出路径
    """a+是可以写也可以在文件后面追加，即在合并两个文件"""
    # k = open(path + outfile, 'a+')
    if (os.path.exists(outfile)):
        os.remove(outfile)
        print('移除文件： ' + outfile)
    with open(outfile, 'a+') as k:
        # org_file_path = []
        for file in infiles:
            org_file = mypath + '/edgelistMergeFile/' + file
            print('org_file：'+org_file)
            # org_file_path.append(org_file)
            with open(org_file) as f:
                # 写入新生成的文件 k.write(f.read()+'\n')
                k.write(f.read().strip()+'\n')
        print('合并完成')

if __name__ == "__main__":
    # 将路径转换为原始字符串，转换方法是在字符串之前写一个“r”，这样，我们就无须添加多个“\”，也能够正常使用这个路径。
    # /home/huganglin/myprogram/Search/my_Algo/TAHRL/Graph_to_Inlink/result
    # cora, zhihu, HepTh citeseer
    merge_file()
