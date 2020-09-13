#ALL_IN_ONE_FeatureSelection_CV_LOO.py						20.07.27
#hur.benjamin@mayo.edu
#
#Do every process at once.
#
#[1] From the dataset of interest (i.e hd4)
#    Divide each dataset into 64 data points (using it for CV)
#    at each data folder, we will have 64 subsets of training set, test set
#[2] feature selection 
#	while i <= 64
#		run mixed effect linear model
#		create GLM with the significant features
#		(note: each iterations might have different set of features)
#		measure performance
#
#[3] final model
#	use every dataset
#	feature selection
#	measure performance
#
#[4] Plot things....


def preprocess (file_name, do_lmer, do_feature_selection):

	data_profile = MLFL_main.access_data().get_dir(file_name)
	
	#run R for those seperated files
	if do_lmer == 1:
		#create folder to store
		MLFL_main.feature_selection().do_lmer(file_name, data_profile)

	if do_feature_selection == 1:
		MLFL_main.feature_selection().extract_sig_features(file_name)

			
def summarize_features(fs_summary_folder):

	if os.path.isdir(fs_summary_folder) == True:
		os.system('rm -r %s' % fs_summary_folder)
		os.system('mkdir %s' % fs_summary_folder)
	else:
		os.system('mkdir %s' % fs_summary_folder)

	hd4_dir = './hd4_qc_matrix/feature_selection'

	hd4_only_list = [hd4_dir]
	integrate_features(fs_summary_folder, hd4_only_list, 'hd4_only', 64)


def integrate_features(fs_summary_folder, file_list, fs_choice, file_splits):
	
	for i in range(1, file_splits + 1):
		for ith_file in file_list:
			cmd = 'cat %s/%s.lmer.out.sig.features >> ./%s/%s.%s.fs' % (ith_file, i, fs_summary_folder, i, fs_choice)
			os.system(cmd)

def preprocess_full_dataset (file_name, do_lmer, do_feature_selection):

	data_profile = MLFL_main.access_data().get_dir(file_name)
	
	#run R for those seperated files
	if do_lmer == 1:
		#create folder to store
		MLFL_validation.do_lmer_full_dataset(file_name, data_profile)

	if do_feature_selection == 1:
		MLFL_validation.extract_sig_features_full_dataset(file_name)


if __name__ == '__main__':

	import sys
	sys.path.insert(1,'../../src')
	sys.path.insert(1, '../../src/machine_learning_public/')

	import os
	import FL
	import MLFL_CV
	import MLFL_main
	import MLFL_plots
	import MLFL_validation
	import LINEAR_MODEL_FL as LMFL
	import numpy as np
	import statistics

	#MANUAL INFORMATION REQUIRED
	file_list = ['hd4_qc_matrix']
	summary_folder = 'fs_summary'
	data_splits = 64

	#DEBUG Thresholds
	#1 = skip process
	#0 = Do process

	#validate the performance of "Feature selection" (sample size 128 = patients 64)
	#Model will use 126 samples to create a model
	#Model will predict DAS28 score using 2 samples
	#Repeating this 64 times
	skip_preprocess = 1
	skip_2nd_preprocess = 1
	skip_model_performance = 0

	#Testing the performance of "Feature selection" with full dataset (sample size 128 + 12  = patients 64 + 12)
	#Model will use 128 samples to create a model
	#Model will predict DAS28-CRP score using 12 samples
	skip_full_model_preprocess = 1
	skip_full_model_2nd_preprocess = 1
	skip_final_model_performance = 0
	
	if skip_preprocess == 0:
		for file_name in file_list:
			print  ("Preprocess to feature selection step #1  > %s" % file_name)
			preprocess(file_name, 1, 1)
		summarize_features(summary_folder)

	if skip_2nd_preprocess == 0:
		hd4_only_list = ['hd4_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(hd4_only_list, 'hd4_fs', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(hd4_only_list, 'hd4_fs', data_splits)
		MLFL_main.feature_selection().full_feature_selection_v2(hd4_only_list, 'hd4_nofs', data_splits)


	#MANUAL INFORMATION REQUIRED
	ml_ready_folders = ['hd4_fs', 'hd4_nofs']
	from sklearn.linear_model import LinearRegression

	if skip_model_performance == 0:
		loo_cv_dict = {}
		
		for folder in ml_ready_folders:
			loo_cv_ae_list = []
			ml_result_folder = '%s/ml_results' % folder

			if os.path.isdir(ml_result_folder) == True:
				os.system('rm -r %s' % ml_result_folder)
				os.system('mkdir %s' % ml_result_folder)
			else:
				os.system('mkdir %s' % ml_result_folder)

			for index in range(1, data_splits + 1):
				ml_ready_file = '%s/%s.ml.ready.txt' % (folder, index)
				ml_ready_test_file = '%s/%s.ml.ready.test.txt' % (folder, index)

				X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
				X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)

				X_train = np.array(X_train)
				y_train = np.array(y_train)
				X_test = np.array(X_test)
				y_test = np.array(y_test)

				lr = LinearRegression()
				data_point_for_plot_dict, AE_list = MLFL_CV.cross_validation().training_model_learning_and_prediction(lr, X_train, y_train, X_test, y_test)
				loo_cv_ae_list.append(AE_list[0])
				loo_cv_ae_list.append(AE_list[1])
				
			loo_cv_dict[folder] = loo_cv_ae_list
			print (len(loo_cv_ae_list))
			print ('----------------------------')
			print ('%s' % folder)
			print ('DataSplits: %s' % data_splits)
			print ('means of AE: %s' % statistics.mean(loo_cv_ae_list))
			print ('stdvs of AE: %s' % statistics.stdev(loo_cv_ae_list))
			print ('----------------------------')

		MLFL_plots.plots().plot_loo_mae_variance_plot(loo_cv_dict, './training_model.mae.summary.pdf', "Indexs of test data", "Mean Absolute Error")


	if skip_full_model_preprocess == 0:
		for file_name in file_list:
			print  ("Preprocess [full dataset] to feature selection step #1  > %s" % file_name)
			preprocess_full_dataset(file_name, 1, 1)

	if skip_full_model_2nd_preprocess == 0:

		#with feature selection
		hd4_only_list = ['hd4_qc_matrix']
		hd4_test_only_list = ['hd4_qc_nan_matrix']

		MLFL_validation.create_full_model_ready_matrix(hd4_only_list, 'hd4_fs', hd4_test_only_list)
		MLFL_validation.full_data_full_feature_selection(hd4_only_list, 'hd4_nofs', hd4_test_only_list)


	if skip_final_model_performance == 0:
		final_model_dict = {}

		for folder in ml_ready_folders:
			loo_cv_mae_list = []
			print ("Final Model Validation > %s" % folder)

			ml_ready_file = '%s/full.ml.ready.txt' % (folder)
			ml_ready_test_file = '%s/full.ml.ready.test.txt' % (folder)

			X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
			X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)

			X_train = np.array(X_train)
			y_train = np.array(y_train)
			X_test = np.array(X_test)
			y_test = np.array(y_test)

			lr = LinearRegression()
			data_point_for_plot_dict, MAE, AE_list = MLFL_CV.cross_validation().validation_model_learning_and_prediction(lr, X_train, y_train, X_test, y_test)
			stdev_MAE = statistics.stdev(AE_list)
			
			final_model_dict[folder] = AE_list
			print (data_point_for_plot_dict)
			print ('----------------------------')
			print ('%s' % folder)
			print ('MAE: %s' % MAE)
			print ("stdev MAE: %s" % stdev_MAE)
			#print (AE_list)
			print ('----------------------------')

			MLFL_plots.plots().draw_pre_observ_scatter_plot(data_point_for_plot_dict, folder)
		MLFL_plots.plots().plot_loo_mae_variance_plot(final_model_dict, './final_model.mae.summary.pdf', "Test Data (patient's single data point)", "Absolute Error |observation - prediction|")

else:
	None
