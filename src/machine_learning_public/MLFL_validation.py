def do_lmer_full_dataset(file_name, data_profile):

		out_dir = './%s' % file_name
		os.system('Rscript ../../src/machine_learning_public/MLR_R_lmer_fulldataset.r %s %s' % (data_profile, out_dir))

def full_data_full_feature_selection(folder_list, summary_folder, test_folder_list):
#NO Feature selection...
	#note:
	#chemID order are different between trainingset and test set.
	#number of chemID are also slightly different. Because some patients do not have values in certain chemicals
	#80% of nan valued chemicals in test set have been removed

	train_profile_dict = {}
	train_chemID_list = []

	train_output_file = '%s/full.ml.ready.txt' % (summary_folder)
	test_output_file = '%s/full.ml.ready.test.txt' % (summary_folder)

	for i in range(len(folder_list)):
		#train
		folder_name = folder_list[i]
		file_name = '%s/full.lmer.df.csv' % (folder_name)

		train_file = open(file_name,'r')
		train_file_readlines = train_file.readlines()

		for i in range(len(train_file_readlines)):
			read = train_file_readlines[i]
			read = read.replace('\n','')
			read = read.replace(',','\t')
			token = read.split('\t')
			if i == 0:
				train_profile_dict['patientID'] = token[1:]
			if i == 4:
				train_profile_dict['DAS28'] = token[1:]
			if i > 4:
				train_profile_dict[token[0]] = token[1:]
				train_chemID_list.append(token[0])

		train_file.close()

	test_profile_dict = {}
	test_chemID_list = []

	for i in range(len(test_folder_list)):
		test_file_name = MLFL_main.access_data().get_dir(test_folder_list[i])
		test_file = open(test_file_name,'r')
		test_file_readlines = test_file.readlines()

		test_output_file = '%s/full.ml.ready.test.txt' % (summary_folder)

		for i in range(len(test_file_readlines)):
			read = test_file_readlines[i]
			read = read.replace('\n','')
			read = read.replace(',','\t')
			token = read.split('\t')
			if i == 0:
				test_profile_dict['patientID'] = token[1:]
			if i == 1:
				test_profile_dict['DAS28'] = token[1:]
			if i > 1:
				test_profile_dict[token[0]] = token[1:]
				test_chemID_list.append(token[0])

		test_file.close()
	
	common_chemID_list = list(set(train_chemID_list) & set(test_chemID_list))

	full_data_full_feature_selection_write_text(train_output_file, train_profile_dict, common_chemID_list)
	full_data_full_feature_selection_write_text(test_output_file, test_profile_dict, common_chemID_list)

	print ("full data No feature selection Done!")

def full_data_full_feature_selection_write_text(file_name, data_dict, common_chemID_list):
	output_txt = open(file_name,'w')

	patientID_list = data_dict['patientID']
	output_txt.write('patientID')

	for patientID in patientID_list:
		output_txt.write('\t%s' % patientID)
	output_txt.write('\n')

	das28_list = data_dict['DAS28']
	output_txt.write('DAS28')

	for das in das28_list:
		output_txt.write('\t%s' % das)
	output_txt.write('\n')

	for chemID in common_chemID_list:
		values = data_dict[chemID]
		output_txt.write(chemID)
		for i in range(len(values)):
			output_txt.write('\t%s' % values[i])
		output_txt.write('\n')
	output_txt.close()


def extract_sig_features_full_dataset(file_name):

	lmer_out_file = '%s/full.lmer.out' % file_name
	output_txt = '%s/feature_selection/full.sig.features' % file_name

	output_txt = open(output_txt,'w')
	mlr_result_dict, chemID_list = LMFL.linear_model_result_manage(lmer_out_file)

	for chemID in chemID_list:
		criteria = mlr_result_dict[chemID][0]
		if criteria == 3 or criteria == 2:
			output_txt.write('%s\n' % chemID)

	output_txt.close()

def create_full_model_ready_matrix(folder_list, summary_folder, test_only_list):

	feature_list_file = '%s/full.feature.list' % (summary_folder)

	if os.path.isfile(feature_list_file) == True:
		os.system('rm %s' % feature_list_file)

	for folder_name in folder_list:
		sig_feature_data = '%s/feature_selection/full.sig.features' % (folder_name)
		cmd = ('echo %s >> ./%s' % (sig_feature_data, feature_list_file))
		os.system(cmd)


	feature_list_file =  open(feature_list_file,'r')
	feature_list_readlines = feature_list_file.readlines()

	#feature lists varies (1~4)
	ith_data_dict = {}
	ith_data_list = []

	ith_data_test_dict = {}
	ith_data_test_list = []
	
	#WE need this to sync the order
	train_chemID_list = []

	for i in range(len(feature_list_readlines)):
		read = feature_list_readlines[i]
		ith_feature_file = read.replace('\n','')

		token = ith_feature_file.split('/')
		folder_name = token[0]

		ith_df_file = '%s/full.lmer.df.csv' % (folder_name)
		ith_data_dict, train_chemID_list = cv_ready_matrix_step_b_submodule(ith_feature_file, ith_df_file, ith_data_dict, train_chemID_list)
	#ith_data_dict > feature selected dict

	train_chemID_list.sort()

	test_chemID_list = []
	#ith_data_dict : feature selected overall dict
	for test_data in test_only_list:
		test_data_file = MLFL_main.access_data().get_dir(test_data)
		test_data_file = open(test_data_file,'r')
		test_data_file_readlines = test_data_file.readlines()

		for i in range(len(test_data_file_readlines)):
			read = test_data_file_readlines[i]
			read = read.replace('\n','')
			token = read.split('\t')
		
			if i == 0:
				ith_data_test_dict['patientID'] = token[1:]
			if i == 1:
				ith_data_test_dict['DAS28'] = token[1:]
			if i > 1:
				ith_data_test_dict[token[0]] = token[1:]
				test_chemID_list.append(token[0])
				
	test_chemID_list.sort()
	#ith_data_test_dict > feature selected test_dict
	if len(test_chemID_list) != len(train_chemID_list):
		print ("------------- %s --------------" % summary_folder)
		print ("Note that the number of chemID of Training set and Test set are different")
		print ("This is not a problem due to our preprocess scheme. But be noted.")
		print ("Training Set : %s" % len(train_chemID_list))
		print ("Test Set : %s" % len(test_chemID_list))
		print ('-------------------------------')
	
	common_chemID_list = list(set(train_chemID_list) & set(test_chemID_list))

	write_ml_ready_matrix(ith_data_dict, common_chemID_list, summary_folder, '')
	write_ml_ready_matrix(ith_data_test_dict, common_chemID_list, summary_folder, '.test')

def write_ml_ready_matrix(ith_data_dict, chemID_list, summary_folder, label):

	file_dir = '%s/full.ml.ready%s.txt' % (summary_folder,label)
	output_txt = open(file_dir,'w')

	patientID_list = ith_data_dict['patientID']
	das28_list = ith_data_dict['DAS28']

	for patientID in patientID_list:
		if patientID != '':
			output_txt.write('\t%s' % patientID)
	output_txt.write('\n')

	output_txt.write('DAS28')
	for value in das28_list:
		if value != '':
			output_txt.write('\t%s' % value)
	output_txt.write('\n')

	for chemID in chemID_list:
		if chemID != 'patientID' and chemID != 'DAS28':
			output_txt.write(chemID)
			value_list = ith_data_dict[chemID]
			for value in value_list:
				output_txt.write('\t%s' % value)
			output_txt.write('\n')
	output_txt.close()


def cv_ready_matrix_step_b_submodule(ith_feature_file, ith_df_file, ith_data_dict, chemID_list):

	ith_feature_file = open(ith_feature_file,'r')
	ith_feature_readlines = ith_feature_file.readlines()

	ith_df_file = open(ith_df_file,'r')
	ith_df_readlines = ith_df_file.readlines()

	sig_feature_list = ['DAS28','patientID']

	#creating full sig feature list
	for i in range(len(ith_feature_readlines)):
		feature_name = ith_feature_readlines[i]
		feature_name = feature_name.replace('\n','')

		if feature_name in sig_feature_list:
			print ("ERROR! in cv_ready_matrix_step_b_submodule")
			quit()
		sig_feature_list.append(feature_name)

	for i in range(len(ith_df_readlines)):
		read = ith_df_readlines[i]
		read = read.replace('\n','')
		token = read.split(',')
		if i == 0:
			ith_data_dict['patientID'] = token
		if i == 4:
			ith_data_dict['DAS28'] = token[1:]
		if i > 4:
			if token[0] in sig_feature_list:
				ith_data_dict[token[0]] = token[1:]
				chemID_list.append(token[0])

	ith_df_file.close()
	ith_feature_file.close()

	return ith_data_dict, chemID_list

if __name__ == "__main__":
	None
else:
	import os
	import sys
	sys.path.insert(1,'../../src')
	import MLFL_main
	import LINEAR_MODEL_FL as LMFL
