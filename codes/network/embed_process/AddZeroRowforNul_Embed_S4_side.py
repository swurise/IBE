import numpy as np

def merge_score():
    '''
    arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    print(list(map(list,zip(*arr))))
    list1=[1,2,3,4]
    list2 = [1, 55, 3, 4]
    list3 = [1, 2, 77, 4]
    list4 = [1, 2, 77, 4]
    ar=[list1,list2,list3,list4]
    print([ [a,b,c,d] for a,b,c,d in zip(*ar)])
# [ np.reshape(a, len(a)),np.reshape(b, len(b)),np.reshape(c, len(c))]
    '''
###转置
    # arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
    # print(arr)
    # x = np.array(arr).transpose()
    # print(x)

    list1=[1,2,3,4]
    list2 = [1, 55, 3, 4]
    print(np.vstack([list1,list2]))

# 读文件里面的数据转化为二维列表,行空填0（100维）
def Trans_File(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表
        # print(column_list)
        len_column_list=len(column_list) # 一行元素为空就填写0
        print('len_column_list:'+len_column_list.__str__())
        if len_column_list == 0 :
            # column_list=[[0]*100]
            # for i in range(100):
            list_source.append([
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 \
                , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 \
                , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 \
                , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 \
                , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 \
                ]);
        else:
            list_source.append(column_list)  # 在末尾追加到list_source

    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j]=(list_source[i][j])
    file1.close()
    # print(list_source)
    # for i in range(len(list_source)):
    #     print ("list_source[i]-", i ," : ", list_source[i])
    return list_source

# 读文件里面的数据转化为二维列表，,行空不处理
def Read_list(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表
        list_source.append(column_list)                # 在末尾追加到list_source
    for i in range(len(list_source)):  # 行数
        for j in range(len(list_source[i])):  # 列数
            list_source[i][j]=(list_source[i][j])
    file1.close()
    # print(list_source)
    # for i in range(len(list_source)):
    #     print ("list_source[i]-", i ," : ", list_source[i])
    return list_source

#保存二维列表到文件
def Save_list(filename0,filename):
    mergeList=Trans_File(filename0) # handle the primary data network_embed.txt flag=0,(filename0, 0)

    file2 = open(filename, 'w')
    for i in range(len(mergeList)):
        for j in range(len(mergeList[i])):
            file2.write(str(mergeList[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
            file2.write('\t')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    file2.close()

if __name__ == "__main__":
    # network_embed.txt ['affairs1,constellation2,economic3,edu4,ent5,fashion6,game7,home8,house9,lottery10,science11,sports12,stock13']
    filename0='/home/huganglin/myprogram/Search/my_Algo/TAHRL/Inlink_to_TopicEmbed/result/cora_embed/cora_embed.txt'
    path="result/cora_embed/"
    filename  = path+"addZeroRow_cora_embed.txt"  #新的嵌入
    Save_list(filename0,filename)