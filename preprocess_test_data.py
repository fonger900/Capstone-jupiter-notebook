import pandas as pd

#colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]

test_set=pd.read_csv('/home/phong/python_files/kdd99_dos_att_10_percent.csv')

#get dos's attribute

#train_set=train_set[colname]

#reduce output to 'normal' and 'attack'
test_labels=test_set['label'].copy()
test_labels[test_labels!='normal']='attack'

#~firstly, we are going to transform all categorical attibute to numeric attribute~

# preprocessing nomial features
import numpy as np
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
le = LabelEncoder()

#preprocess 'service' attribute (having large number of unique value)
#Methodology: calculating the ratio of 'attack''s records of one service then replace service's name with the calculated values
value_list = le.fit(test_set['service'])
for element in value_list.classes_:
    N = test_set[test_set['service']==element].shape[0]#number of instance equal to 'element' in 'service''s column
    Np = test_set[(test_set['service']==element) & (test_set['label']!='normal')].shape[0]#number of instance equal to 'element' in 'service''s column and have label of 'attack'
    A=Np/N
    test_set.loc[test_set['service']==element,'service']=A
    
#preprocessing 'flag' and 'protocol_type' attribute (having few number of unique value)
a = pd.get_dummies(test_set[['flag','protocol_type']])
test_set = pd.concat([test_set,a],axis=1)
test_set=test_set.drop(['Unnamed: 0','flag','protocol_type'],axis=1)
#train_set['flag']=le.fit_transform(train_set['flag'])

#~/~

#exclude the 'label' attribute from set
test_set.drop(['label'],inplace=True,axis=1)
    
#feature scaling
test_set=test_set.astype(float)
from sklearn.preprocessing import MinMaxScaler
for each_column in test_set:
    test_set[each_column] = MinMaxScaler().fit_transform(test_set[each_column].values.reshape(len(test_set),-1))

#save to file
full_test_set = pd.concat([test_set,test_labels],axis=1)
full_test_set.to_csv('/home/phong/python_files/preprocessed_kdd99_dos_att_10_percent.csv')    

#transform label to numeric representation
test_labels = le.fit_transform(test_labels)

#train model
#from sklearn.neighbors import KNeighborsClassifier
#clf=KNeighborsClassifier(n_neighbors=5,algorithm='ball_tree',leaf_size=500)
#from time import time
#t0=time()
#clf.fit(features,labels)
#tt=time()-t0
#print('classifier trained in {} seconds'.format(round(tt,3)))