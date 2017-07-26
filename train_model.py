from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier()

clf=clf.fit(train_set,train_labels)

clf.predict(test_set)

clf.score(test_set,test_labels)
