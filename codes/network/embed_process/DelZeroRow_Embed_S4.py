import numpy as np

# 读文件里面的数据转化为二维列表,行空填0（100维）
def Trans_File(filename):
    file1 = open(filename, "r")
    list_row =file1.readlines()
    list_source = []
    for i in range(len(list_row)):
        column_list = list_row[i].strip().split()  # 每一行split后是一个列表
        # print(column_list)
        len_column_list=len(column_list)
        print('len_column_list:'+len_column_list.__str__())
        if len_column_list == 0:
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
        # print(i.__str__()+':'+column_list.__str__())
        # print(i.__str__() + ':' + column_list[20])
        if column_list[20].strip()=='0'.strip(): # 任以判断一个元素（假定是20号元素），如果是0，就填写空
            list_source.append('')
        else:
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
    mergeList=Read_list(filename0) # handle the primary data network_embed.txt flag=0,(filename0, 0)

    file2 = open(filename, 'w')
    for i in range(len(mergeList)):
        for j in range(len(mergeList[i])):
            file2.write(str(mergeList[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
            file2.write('\t')                          # 相当于Tab一下，换一个单元格
        file2.write('\n')                              # 写完一行立马换行
    file2.close()

if __name__ == "__main__":
    # cora, zhihu, HepTh
    dataset = "cora"   # 修改路径处 1/2
    # ['affairs1,constellation2,economic3,edu4,ent5,fashion6,game7,home8,house9,lottery10,science11,sports12,stock13']
    topicname = "stock13"  #  带数字编号 修改主题处 2/2

    filename0 = "result/"+dataset+"_embed/"+dataset+"_Merge_to_Embed_"+topicname+"_M100.txt"  #旧的嵌入
    filename  = "result/"+dataset+"_embed/"+dataset+"_Merge_to_Embed_"+topicname+"_MNZR.txt"  #新的嵌入 noZeroRow
    Save_list(filename0,filename)
    print('filename0:', filename0,'filename:', filename)