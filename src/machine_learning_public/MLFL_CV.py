class cross_validation:

	#For performance measure data set
	#For Final dataset
	#designed to obtain "training_X" and "training y")
	def get_X_y(self, input_file):
		
		data_df = pd.read_csv(input_file,sep="\t", index_col=0)
		data_df = data_df.T  #tilt data

		y = data_df.iloc[:,0]
		X = data_df.iloc[:,1:]

		return X, y

	#For Final dataset
	#designed to obtain "test y"
	#This function is designed because the "Final datset:test set" has different charateristics compare to the performance measurement dataset
	def get_test_X_y(self, input_file):
		
		data_df = pd.read_csv(input_file,sep="\t", index_col=0)
		data_df = data_df.T  #tilt data

		y = data_df.iloc[:,0]
		X = data_df.iloc[:,1:]

		return X, y

	#Run model with performance measurement dataset
	#Designed for Linear Regression.
	#Not sure whether this function will work on other models.
	def training_model_learning_and_prediction(self, model, X_train, y_train, X_test, y_test):

		test_count = 1
		
		data_point_for_plot_dict = {}
		
		model_fit = model.fit(X_train, y_train)
		prediction = model_fit.predict(X_test)
		observed_value = y_test
	
		AE_list = (abs(prediction - observed_value))

		try :
			data_point_for_plot_dict['observe'].append(observed_value)
			data_point_for_plot_dict['predict'].append(prediction)
		except KeyError:
			data_point_for_plot_dict['observe'] = [observed_value]
			data_point_for_plot_dict['predict'] = [prediction]
			
		test_count = test_count + 1

		return data_point_for_plot_dict, AE_list

	#Run model with final dataset
	#Designed for Linear Regression.
	def validation_model_learning_and_prediction(self, model, X_train, y_train, X_test, y_test):

		AE_list = []
		
		data_point_for_plot_dict = {}
		
		model_fit = model.fit(X_train, y_train)
		prediction_list = model_fit.predict(X_test)
		observed_value_list = y_test
	
		MAE = mean_absolute_error(observed_value_list, prediction_list)

		for i in range(len(observed_value_list)):

			observed_value = observed_value_list[i]
			prediction_value = prediction_list[i]
			AE = abs(observed_value - prediction_value)
			AE_list.append(AE)

			try :
				data_point_for_plot_dict['observe'].append(observed_value)
				data_point_for_plot_dict['predict'].append(prediction_value)
			except KeyError:
				data_point_for_plot_dict['observe'] = [observed_value]
				data_point_for_plot_dict['predict'] = [prediction_value]
		
		return data_point_for_plot_dict, MAE, AE_list

	def get_index_list(self, loo_mae_list):
		set_index_list = []
		for i in range(len(loo_mae_list)):
			set_index_list.append(i+1)
		return set_index_list

if __name__ == '__main__':

	print ('Not meant to be run')
else:

	import pandas as pd
	import numpy as np
	from sklearn.metrics import mean_absolute_error
	from sklearn import metrics
	import statistics
		
	print ('Loading MLFL_CV')
