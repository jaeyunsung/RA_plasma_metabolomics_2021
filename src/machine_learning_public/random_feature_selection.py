#random_feature_selection.py				20.01.29
#hur.benjamin@mayo.edu
#
#Gain distribution of MAE from random features.
#
#Input: selective feature matrix
#
#[1] gain N random feature sets. N is the same size of the input feature
#[2] Iterate 10000 times
#[3]	at each iteration, 
#          -obtain mean of MAE
#          -list of MAEs
#Output: 
#1st line, 
#1st column: mean of mean of maes, 2nd column ~ N column: mean of maes 
#2nd line ~ 10000 line (At each iteration)

if __name__ == '__main__':

	import sys
	import numpy as np
	import pandas as pd
	import random
	import statistics
	import operator
	from sklearn.linear_model import LinearRegression
	from sklearn.metrics import mean_absolute_error
	from scipy.stats import ttest_ind
	from scipy.stats import ttest_1samp
	from scipy.stats import wilcoxon
	from scipy.stats import spearmanr
	import seaborn as sns
	import matplotlib.pyplot as plt

	#customized libraries
	sys.path.insert(1, '/Users/m221138/RA_project/code/machine_learning_r2/')
	sys.path.insert(1,'/Users/m221138/RA_project/code')
	sys.path.insert(1, '/Users/m221138/RA_project/code/feature_selection')
	import FL
	import MLFL_CV
	import MLFL_main
	import MLFL_plots
	import MLFL_validation
	import LINEAR_MODEL_FL as LMFL

	train_profile_file = sys.argv[1]
	test_profile_file = sys.argv[2]
	feature_size = int(sys.argv[3])
	
	X_train, y_train = MLFL_CV.cross_validation().get_X_y(train_profile_file)
	X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(test_profile_file)
	r, c = X_train.shape

	chemID_list = list(X_train.columns)
	idx = np.arange(0, c)

	sfeature_AE_file = '/Users/m221138/RA_project/analysis/all_in_one_r2/random_feature/hd4_51_feature.mae.txt'
	sfeature_AE_list = [float(line.rstrip('\n')) for line in open(sfeature_AE_file)]

	rfeature_AE_list = []
#	plot_output = '/Users/m221138/RA_project/analysis/all_in_one_r2/random_feature/figure.pdf'

	rs_log = '/Users/m221138/RA_project/analysis/all_in_one_r2/random_feature/rs.log.txt'
	rs_log_txt = open(rs_log,'w')

	count = 0
	random_iter = 100000
	another_count = 0
	rs_log_txt.write("Total Iterations:%s\n" % random_iter)
	rs_log_txt.write("Iter\tSelectedRandomFeatures\tcorrelation\tPvalue\n")
	for i in range(random_iter):

		subset_idx_list = random.choices(idx, k=feature_size)
		random_feature_list = [chemID_list[subset_idx] for subset_idx in subset_idx_list]

		rX_train = X_train[random_feature_list]
		rX_test = X_test[random_feature_list]


		rX_train = np.array(rX_train)
		y_train = np.array(y_train)

		rX_test = np.array(rX_test)
		y_test = np.array(y_test)

		lr = LinearRegression()
		data_point_dict, MAE, AE_list = MLFL_CV.cross_validation().validation_model_learning_and_prediction(lr, rX_train, y_train, rX_test, y_test)
		corr, pvalue = spearmanr(data_point_dict["predict"], data_point_dict["observe"])

		if pvalue < 0.05:
			print ("#ITER:%s, Significant pvalue by random chance: %s / %s " % (i, another_count, random_iter))
			another_count = another_count + 1
			if corr > 0.685:
				print ("#ITER:%s, Significant pvalue & better corrlation by random chance: %s / %s : %s" % (i, count, random_iter, corr))
				count = count + 1
		rs_log_txt.write("#%s\t%s\t%s\t%s\n" % (i, random_feature_list, corr, pvalue))
	rs_log_txt.close()
#	main_plot = sns.distplot(rfeature_AE_list, hist=False, rug=True, label="Randomly selected (n=51) chemicals (i= 1000)")
#	main_plot.axvline(sAE_mean, 0, 0.5, color="r", label="AE of purposing features (n=51)")
#	main_plot.legend(loc="upper right")
#	main_plot.set(xlabel="AE of DAS28", ylabel="Density")
#	main_plot.get_figure()
#	main_plot.figure.savefig(plot_output)
#	main_plot.get_figure().clf()
	



		

