
def train_model():
    #load
    import pandas as pd
    train_set = pd.read_csv('dataset/preprocessed_kdd99_dos.csv')
    
    #train
    from sklearn.tree import DecisionTreeClassifier
    clf = DecisionTreeClassifier()
    train_label = train_set['label'].copy()
    train_set.drop(['label','Unnamed: 0'],inplace=True,axis=1)
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    train_label = le.fit_transform(train_label)
    #set timer
    from time import time
    t0=time()
    clf=clf.fit(train_set,train_label)
    tt=time()-t0
    print('classifier trained in {} seconds'.format(round(tt,3)))
    
    #save model
    from sklearn.externals import joblib
    joblib.dump(clf, 'kdd_model.pkl')
    print 'save as kdd_model.pkl'
    
train_model()