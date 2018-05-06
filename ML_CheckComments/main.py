import utils
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, roc_auc_score

def NB_model():
	train_data,test_data = utils.prepare_data()
	print('训练集有{}条记录。'.format(len(train_data)))
	print('测试集有{}条记录。'.format(len(test_data)))
	X_train, X_test = utils.feature_engineering(train_data, test_data)
	print('共有{}维特征。'.format(X_train.shape[1]))
	y_train = train_data['label'].values
	y_test = test_data['label'].values
    #数据建模
	nb_model = GaussianNB()
	nb_model.fit(X_train,y_train)
	y_pred = nb_model.predict(X_test)
	print('准确率：',accuracy_score(y_test,y_pred))

def SVC_model():
	train_data,test_data = utils.prepare_data()
	print('训练集有{}条记录。'.format(len(train_data)))
	print('测试集有{}条记录。'.format(len(test_data)))
	X_train, X_test = utils.feature_engineering(train_data, test_data)
	print('共有{}维特征。'.format(X_train.shape[1]))
	y_train = train_data['label'].values
	y_test = test_data['label'].values
    #数据建模
	c_values = [0.0001, 1, 10000]
	for c_value in c_values:
		svm_model = SVC(C=c_value)
		svm_model.fit(X_train,y_train)
		y_pred = svm_model.predict(X_test)
		print('准确率：',accuracy_score(y_test,y_pred))



if __name__ == '__main__':
	#SVC_model()
	NB_model()