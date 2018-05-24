import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
import tensorflow as tf
# from tensorflow.python.ops import rnn, rnn_cell
import csv
from sklearn.feature_extraction import DictVectorizer
from tensorflow.python.framework.tensor_shape import scalar

df = pd.read_csv('D:/after_clustering_test1.csv')
target_value = df["target_value"]

#Stored continuous value as a dict
featureConCols = ['ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','turnover','rate1','rate2','rate3','pos1','pos2','pos3','amt1','amt2','amt3']
datafeatureConCols = df[featureConCols]
X_dictCon = datafeatureConCols.T.to_dict().values()

#Stored dispersed value as a dict
featureDisCols = ['Mon','Tues','Wed','Thurs','Fri']
datafeatureDisCols = df[featureDisCols]
X_dictDis = datafeatureDisCols.T.to_dict().values()

vec = DictVectorizer(sparse=False)
X_dictCon = vec.fit_transform(X_dictCon)
X_dictDis = vec.fit_transform(X_dictDis)

#standardization
from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(X_dictCon)
X_dictCon = scaler.transform(X_dictCon)
X_ves = np.hstack((X_dictCon,X_dictDis))
X_ves = np.array(X_ves)
Y_ves = df[['target_up_5per','target_up','target_down_5per','target_down']]
Y_ves = np.array(Y_ves)


from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.multiclass import OneVsRestClassifier
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

#Feature selection method based on tree model
#X_ves = SelectFromModel(GradientBoostingClassifier()).fit_transform(X_ves,df['target_value'])

#Feature selection method based on penalty term(penalty="l1")
#X_ves = SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(X_ves,df['target_value'])


#Feature selection method based on penalty term(penalty="l2")
#X_ves = SelectFromModel(LogisticRegression(C=0.1)).fit_transform(X_ves,df['target_value'])


#Wrapper
X_ves = RFE(estimator=LogisticRegression(), n_features_to_select=4).fit_transform(X_ves,df['target_value'])

#PCA
X_ves = PCA(n_components=2).fit_transform(X_ves)


 


#sklearn LogisticRegression
from sklearn import linear_model
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC    
from sklearn import tree    
from sklearn.ensemble import RandomForestClassifier  
from sklearn.neighbors import KNeighborsClassifier 


#KNN   
#clf = KNeighborsClassifier()  

#RandomForestClassifier
#clf = RandomForestClassifier(n_estimators=8)

#decisionTree
#clf = OneVsRestClassifier(tree.DecisionTreeClassifier())

#SVC
clf = OneVsRestClassifier(SVC(kernel='rbf', probability=True))

#LogisticRegression
#clf = OneVsRestClassifier(linear_model.LogisticRegression(C=1.0,penalty='l1',tol = 1e-6,solver='liblinear',multi_class='ovr'))

clf.fit(X_ves, Y_ves)

#testDataSet
datatest = pd.read_csv('D:/after_clustering_test1.csv')
targetTest = df["target"]

#Stored continuous value as a dict
testfeatureConCols = ['ma5','ma10','ma20','v_ma5','v_ma10','v_ma20','turnover','rate1','rate2','rate3','pos1','pos2','pos3','amt1','amt2','amt3']
testdatafeatureConCols = datatest[testfeatureConCols]
testX_dictCon = testdatafeatureConCols.T.to_dict().values()

#Stored dispersed value as a dict
testfeatureDisCols = ['Mon','Tues','Wed','Thurs','Fri']
testdatafeatureDisCols = datatest[testfeatureDisCols]
testX_dictDis = np.array(testdatafeatureDisCols)
#testX_dictDis = testdatafeatureDisCols.T.to_dict().values()

testX_dictCon = vec.fit_transform(testX_dictCon)
#testtX_dictDis = vec.fit_transform(testX_dictDis)

#standardization
from sklearn import preprocessing
scaler = preprocessing.StandardScaler().fit(testX_dictCon)
testX_dictCon = scaler.transform(testX_dictCon)
testX_dictDis = np.array(testX_dictDis)
testX_ves = np.concatenate((testX_dictCon,testX_dictDis), axis = 1)
testY_ves = datatest[['target_up_5per','target_up','target_down_5per','target_down']]
testY_ves = np.array(testY_ves)

#predictions = clf.predict(testX_ves)
#result=pd.DataFrame(predictions)
#result.to_csv('D:/testDataSet/result.csv')

#plot learning curve
from sklearn.learning_curve import learning_curve

def plot_learning_curve(estimator,title,X,y,ylin = None,cv = None,n_jobs = 1,
                        train_sizes=np.linspace(.05,1.,30),verbose = 0,plot = True):
    print(len(X))
    print(len(y))
    train_sizes,train_scores ,test_scores = learning_curve(estimator, X, y, train_sizes=train_sizes, cv=10,  n_jobs=n_jobs, verbose=verbose)
    
    train_scores_mean = np.mean(train_scores,axis=1)
    train_scores_std = np.std(train_scores,axis=1)
    test_scores_mean = np.mean(test_scores,axis=1)
    test_scores_std = np.std(test_scores,axis=1)
    
    if(plot):
        plt.figure()
        plt.title(title)
        if ylin is not None:
            plt.ylim(ylin)
        plt.xlabel(u'trainset_count')
        plt.ylabel(u'score')
        plt.gca().invert_yaxis()
        plt.grid()
        
        plt.fill_between(train_sizes, train_scores_mean-train_scores_std, train_scores_mean+train_scores_std, alpha=0.1, color='b')
        plt.fill_between(train_sizes, test_scores_mean-test_scores_std, test_scores_mean+test_scores_std, alpha=0.1, color='r')
        plt.plot(train_sizes,train_scores_mean,'o-',color='b',label=u'scores of trainSet')
        plt.plot(train_sizes,test_scores_mean,'o-',color='r',label=u'scores of testSet')
        
        plt.legend(loc='best')
        
        plt.draw()
        plt.gca().invert_yaxis()
        plt.show()
        
        
    midpoint = ((train_scores_mean[-1]+train_scores_std[-1])+(test_scores_mean[-1]+test_scores_std[-1]))/2
    diff = ((train_scores_mean[-1]+train_scores_std[-1])-(test_scores_mean[-1]+test_scores_std[-1]))/2
    return midpoint,diff
        
plot_learning_curve(clf, u"learningCurve", X_ves, Y_ves)
    
    
    
