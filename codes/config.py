import os
basepath = os.path.abspath(os.path.join(os.getcwd(), "../../../datasets"))
# basepath = '/home/huganglin/myprogram/MyPro/IBE/datasets'

psi_coefficient_dict = {
    'blogCatalog-DeepWalk':4 ,'blogCatalog-HOPE':4 ,'blogCatalog-LAP':4 ,'blogCatalog-LINE':4 ,'blogCatalog-Node2vec':4 ,
    'citeseer-DeepWalk':4 ,'citeseer-HOPE':4 ,'citeseer-LAP':4 ,'citeseer-LINE':4 ,'citeseer-Node2vec':2 ,
    'cora-CANE':4 ,'cora-DeepWalk':1 ,'cora-HOPE':4 ,'cora-LAP':4 ,'cora-LINE':4 ,'cora-Node2vec':4 ,
    'wiki-DeepWalk':4 ,'wiki-HOPE':4 ,'wiki-LAP':4 ,'wiki-LINE':7 ,'wiki-Node2vec':4 ,
    'zhihu-CANE':4 ,'zhihu-DeepWalk':4 ,'zhihu-HOPE':6 ,'zhihu-LAP':4 ,'zhihu-LINE':4 ,'zhihu-Node2vec':2   }

psi_coefficient_list = [-5,-1,0,1,2,3,4,5,6,7,8,9,15,25]

datasets = ['blogCatalog','citeseer','cora','wiki','zhihu']
methods = ['CANE','DeepWalk','HOPE','LAP','LINE','Node2vec']



# datasets = ['blogCatalog','citeseer','cora_feature2708','cora','wiki','zhihu']
# methods = ['CANE','DeepWalk','HOPE','LAP','LINE','Node2vec','SDNE','TADW']




