from sklearn.externals import joblib
joblib.dump(clf, 'kdd_model.pkl')
clf = joblib.load('kdd_model.pkl') 
