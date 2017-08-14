
import pandas as pd

#colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","serror_rate","rerror_rate","diff_srv_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_srv_serror_rate","label"]
# get desired subset

#dset = pd.read_csv('/home/phong/study/capstone_project/dataset/kddcup.data_10_percent_corrected',header=None,names=colname)
#colname = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","count","label"]
#dset = dset[colname]
#dset.to_csv('dataset/kdd_10percent_corrected.csv')

test_set=pd.read_csv('dataset/kdd_dos_data.csv')
#test_set=test_set[colname]
#get dos's attribute

#train_set=train_set[colname]

#reduce output to 'normal' and 'attack'
test_labels=test_set['label'].copy()
test_labels[test_labels!='normal.']='attack'

#~firstly, we are going to transform all categorical attibute to numeric attribute~

# preprocessing nomial features
#import numpy as np
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()

#preprocess 'service' attribute (having large number of unique value)
#Methodology: calculating the ratio of 'attack''s records of one service then replace service's name with the calculated values
value_list = le.fit(test_set['service'])
for element in value_list.classes_:
    N = test_set[test_set['service']==element].shape[0]#number of instance equal to 'element' in 'service''s column
    Np = test_set[(test_set['service']==element) & (test_set['label']!='normal')].shape[0]#number of instance equal to 'element' in 'service''s column and have label of 'attack'
    A=Np/N
    test_set.loc[test_set['service']==element,'service']=A
#transform 'protocol_type' attribute
import numpy as np

test_set['tcp_proto'] = test_set['protocol_type']
test_set.loc[test_set['tcp_proto']!='tcp','tcp_proto']=0
test_set.loc[test_set['tcp_proto']=='tcp','tcp_proto']=1

test_set['udp_proto'] = test_set['protocol_type']
test_set.loc[test_set['udp_proto']!='udp','udp_proto']=0
test_set.loc[test_set['udp_proto']=='udp','udp_proto']=1

test_set['icmp_proto'] = test_set['protocol_type']
test_set.loc[test_set['icmp_proto']!='icmp','icmp_proto']=0
test_set.loc[test_set['icmp_proto']=='icmp','icmp_proto']=1

#transform 'flag' attribute
flags = np.array(['S0','S1','SF','REJ','S2','S3','RSTO','RSTR','RSTOS0','RSTRH','SH','SHR','OTH'])
for i in flags:
    colname = 'flag_{!s}'.format(i)
    test_set[colname] = test_set['flag']
    test_set.loc[test_set[colname]!=i,colname]=0
    test_set.loc[test_set[colname]==i,colname]=1

#preprocessing 'flag' and 'protocol_type' attribute (having few number of unique value)
test_set=test_set.drop(['Unnamed: 0','protocol_type','flag'],axis=1)

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
full_test_set.to_csv('dataset/preprocessed_kdd99_dos.csv')    

#transform label to numeric representation
test_labels = le.fit_transform(test_labels)
#print 'done'
