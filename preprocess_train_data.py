import pandas as pd

#colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]

train_set=pd.read_csv('~/dataset/dos_kdd99.csv')

#reduce output to 'normal' and 'attack'
train_labels=train_set['label'].copy()
train_labels[train_labels!='normal']='attack'

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
    Np = train_set[(train_set['service']==element) & (train_set['label']!='normal')].shape[0]#number of instance equal to 'element' in 'service''s column and have label of 'attack'
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
full_train_set.to_csv('~/dataset/preprocessed_dos_kdd99.csv') 

#transform label to numeric representation
train_labels = le.fit_transform(train_labels)

#train model
#from sklearn.neighbors import KNeighborsClassifier
#clf=KNeighborsClassifier(n_neighbors=5,algorithm='ball_tree',leaf_size=500)
#from time import time
#t0=time()
#clf.fit(features,labels)
#tt=time()-t0
#print('classifier trained in {} seconds'.format(round(tt,3)))