import pandas as pd

def preprocess_data(log_data):
    
#~firstly, we are going to transform all categorical attibute to numeric attribute~

# preprocessing nomial features
#preprocess 'service' attribute (having large number of unique value)
#Methodology: calculating the ratio of 'attack''s records of one service then replace service's name with the calculated values
    value_list = log_data['service'].unique()
    N = log_data['service'].count()#number of instance equal to 'element' in 'service''s column
    for element in value_list:
        Np = log_data[log_data['service']==element].shape[0]#number of instance equal to 'element' in 'service''s column
        A=Np/N
        log_data.loc[log_data['service']==element,'service']=A
#transform 'protocol_type' attribute
    import numpy as np
    protocols = np.array(['tcp','udp','icmp'])
    for i in protocols:
        colname = '{!s}_proto'.format(i)
        log_data[colname] = log_data['protocol_type']
        log_data.loc[log_data[colname]!=i,colname]=0
        log_data.loc[log_data[colname]==i,colname]=1
#transform 'flag' attribute
    flags = np.array(['S0','S1','SF','REJ','S2','S3','RSTO','RSTR','RSTOS0','RSTRH','SH','SHR','OTH'])
    for i in flags:
        colname = 'flag_{!s}'.format(i)
        log_data[colname] = log_data['flag']
        log_data.loc[log_data[colname]!=i,colname]=0
        log_data.loc[log_data[colname]==i,colname]=1

#preprocessing 'flag' and 'protocol_type' attribute (having few number of unique value)
    log_data=log_data.drop(['Unnamed: 0','protocol_type','flag'],axis=1)

#feature scaling
    log_data=log_data.astype(float)
    from sklearn.preprocessing import MinMaxScaler
    for each_column in log_data:
        log_data[each_column] = MinMaxScaler().fit_transform(log_data[each_column].values.reshape(len(log_data),-1))
    return log_data
    
def predict_label(pre_log_data):
    from sklearn.externals import joblib
    clf = joblib.load('kdd_model.pkl')
    label = clf.predict(pre_log_data)
    return label

def calculate_threshold(log_data):
    threshold = log_data['count'][log_data['label']==0].mean()
    return threshold
    
def main():
    log_data=pd.read_csv('out.csv')
    pre_log_data = log_data.copy()
    pre_log_data = preprocess_data(pre_log_data)
    label = predict_label(pre_log_data)
    log_data['label'] = label
    log_data.to_csv('labeled_kdd_dos.csv')
    threshold = calculate_threshold(log_data)
    
    print 'threshold is: {!s}'.format(threshold)
    print 'done'
    
    
main()