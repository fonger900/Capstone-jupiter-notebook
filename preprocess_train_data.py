import pandas as pd

#col_names = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root","num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login","count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
#kdd = pd.read_csv('/home/duyphong_dinh56/dataset/kddcup.data_10_percent',header=None, names=col_names')#read dataset
    
#dos_col_names = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]
#kdd[dos_col_names].to_csv('/home/duyphong_dinh56/dataset/kddcup_dos.csv')#write dataset to new csv file


train_set=pd.read_csv('/home/duyphong_dinh56/dataset/kddcup_dos_10percent.csv')

#reduce output to 'normal' and 'attack'
train_labels=train_set['label'].copy()
train_labels[train_labels!='normal.']='attack.'

#~firstly, we are going to transform all categorical attibute to numeric attribute~

# preprocessing nomial features
import numpy as np
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
le = LabelEncoder()

#preprocess 'service' attribute (having large number of unique value)
#Methodology: calculating the ratio of 'attack''s records of one service then replace service's name with the calculated values
value_list = le.fit(train_set['service'])
for element in value_list.classes_:
    N = train_set[train_set['service']==element].shape[0]#number of instance equal to 'element' in 'service''s column
    Np = train_set[(train_set['service']==element) & (train_set['label']!='normal.')].shape[0]#number of instance equal to 'element' in 'service''s column and have label of 'attack'
    A=Np/N
    train_set.loc[train_set['service']==element,'service']=A
    
#preprocessing 'flag' and 'protocol_type' attribute (having few number of unique value)
a = pd.get_dummies(train_set[['flag','protocol_type']])
train_set = pd.concat([train_set,a],axis=1)
train_set=train_set.drop(['Unnamed: 0','flag','protocol_type'],axis=1)
#train_set['flag']=le.fit_transform(train_set['flag'])

#~/~


#exclude the 'label' attribute from set
train_set.drop(['label'],inplace=True,axis=1)

#drop redundant feature
train_set.drop(['flag_OTH'],inplace=True,axis=1)

#feature scaling
train_set=train_set.astype(float)
from sklearn.preprocessing import MinMaxScaler
for each_column in train_set:
    train_set[each_column] = MinMaxScaler().fit_transform(train_set[each_column].values.reshape(len(train_set),-1))

    

#save to file    
full_train_set = pd.concat([train_set,train_labels],axis=1)
full_train_set.to_csv('/home/duyphong_dinh56/dataset/preprocessed_kdd99_dos_testset.csv') 

#transform label to numeric representation
#train_labels = le.fit_transform(train_labels)

#train model
#from sklearn.neighbors import KNeighborsClassifier
#clf=KNeighborsClassifier(n_neighbors=5,algorithm='ball_tree',leaf_size=500)
#from time import time
#t0=time()
#clf.fit(features,labels)
#tt=time()-t0
#print('classifier trained in {} seconds'.format(round(tt,3)))
