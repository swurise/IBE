# 根据节点分类标签，给节点归入不同的标签类subV
#####加载配置文件 modify by hugl 2020-8-31######
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../..")))
from  config import *
#######################

# 扫描标签分类文件，找出最大分类标签
def read_node_maxLabel(filename):
    maxLabel = 0
    with open(filename, 'r') as fin:
        while 1:
            l = fin.readline()
            if l == '':
                break
            # modify by huganglin 2020/5/20 #
            vec = l.strip().split()
            for i in vec[1:]:
                if(int(maxLabel)<int(i)): maxLabel=i #分类标签最大数
    return int(maxLabel)

# 扫描标签分类文件，找出分类标签个数，如果标签序列从0开始，标签个数比就比最大值多1，
# 但标签个数函数可以求不是序列的标签
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

def read_node_label_subVzi(filename,intZi):
  with open(filename, 'r') as fin:
    liNodeZi = []
    # for label in labelFile.readlines(): # 与以下while语句等效
    while 1:
        l = fin.readline()
        if l == '':
            break
        # modify by huganglin 2020/5/20 #
        vec = l.strip().split()
        # if l[0].strip() != '':  #有可能遇到空行需要处理
        #     vec = l.strip().split()
        # else:
        #     continue
        # #
        # print(vec[0])
        for i in vec[1:]:
            if(intZi==int(i)): liNodeZi.append(vec[0])
    return liNodeZi

#保存二维列表到文件
def Save_list(liNodeZi,file_SUBV):
    import os
    os.makedirs(file_SUBV[:file_SUBV.rfind('/') + 1], exist_ok=True)  # 保存前目录不存在就创建文件夹,exist_ok=True存在不创建

    with open(file_SUBV, 'w') as fsubVZi:
        for j in liNodeZi:
            fsubVZi.write(str(j))  # write函数不能写int类型的参数，所以使用str()转化
            fsubVZi.write(' ')                          # 相当于Tab一下，换一个单元格
            # fsubVZi.write('\n')                              # 写完一行立马换行

if __name__ == "__main__":
    # zi=26
    # liNodeZi=read_node_label('/home/huganglin/myprogram/Network/comm_Algo/OpenNE-master/data/blogCatalog/bc_labels.txt',zi)
    # filename1 = '/home/huganglin/myprogram/Network/comm_Algo/OpenNE-master/data/blogCatalog/SUBV/subV'+str(zi).strip()+'.txt'
    # # os.makedirs("filename1", exist_ok=True)
    labelfile=mypath+'/node_labels.txt'
    liZi=list_Node_Label_Class(labelfile)
    print(dataset+'标签类数：'+liZi.__str__())
    for zi in liZi:
        liNodesubVzi=read_node_label_subVzi(labelfile,int(zi.strip()))
        file_SUBV =mypath+'/SUBV/subV'+str(zi).strip()+'.txt'
        Save_list(liNodesubVzi,file_SUBV)
        print(zi)
        # print(liNodeZi)

