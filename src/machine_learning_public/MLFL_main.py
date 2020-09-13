class access_data:

	#if you have your own data.locations file, modify this directory
	data_profile = '../../src/machine_learning_public/file_locations.txt'
	data_profile_readlines = open(data_profile,'r').readlines()

	def search_module(self, data_type):
		data_profile_readlines = self.data_profile_readlines

		for i in range(len(data_profile_readlines)):
			read = data_profile_readlines[i]
			read = read.replace('\n','')
			token = read.split('\t')
			if token[0] == data_type:
				dir_of_interest = token[1]
				break
		return dir_of_interest

	def get_dir(self, data_type):
		dir_of_interest = self.search_module(data_type)
		return dir_of_interest


class feature_selection:

	def full_feature_selection_v2(self, folder_list, summary_folder, data_splits):
	#Feature selection scheme for "without feature selection"
	#misleading function name

		if os.path.isdir(summary_folder) == True:
			os.system('rm -r %s' % summary_folder)
			os.system('mkdir %s' % summary_folder)
		else:
			os.system('mkdir %s' % summary_folder)

		for index in range(1, data_splits + 1):
		#i = 1~ 64
			train_profile_dict = {}
			test_profile_dict = {}
			chem_ID_list = []
			patientID_list = []
			train_output_file = '%s/%s.ml.ready.txt' % (summary_folder, index)
			test_output_file = '%s/%s.ml.ready.test.txt' % (summary_folder, index)

			for folder_name in folder_list:
			#i = 1~4
				file_name = '%s/%s.lmer.df.csv' % (folder_name, index)
				train_profile_dict = self.full_feature_selection_sub_function_v2(file_name, train_profile_dict)

				file_name = '%s/%s.lmer.df.test.csv' % (folder_name, index)
				test_profile_dict = self.full_feature_selection_sub_function_v2(file_name, test_profile_dict)

			self.full_feature_selection_v2_write_text(train_output_file, train_profile_dict)
			self.full_feature_selection_v2_write_text(test_output_file, test_profile_dict)
		print ("No feature selection Done!")

	def full_feature_selection_sub_function_v2(self, file_name, profile_dict):

		open_file = open(file_name,'r')
		file_readlines = open_file.readlines()

		for i in range(len(file_readlines)):
			read = file_readlines[i]
			read = read.replace(',','\t')
			token = read.split('\t')
			if i == 0:
				patientID_list = token[1:]
				profile_dict['patientID'] = token[1:]
			if i == 4:
				das28_list = token[1:]
				profile_dict['DAS28'] = token[1:]
			if i > 4:
				profile_dict[token[0]] = token[1:]

		open_file.close()
		return profile_dict

	def full_feature_selection_v2_write_text(self, file_name, profile_dict):
		output_txt = open(file_name,'w')
		for key in list(profile_dict.keys()):
			values = profile_dict[key]
			output_txt.write(key)
			for i in range(len(values)):
				output_txt.write('\t%s' % values[i])
		output_txt.close()

	def full_feature_selection(self, folder_list, summary_folder, data_splits):

		if os.path.isdir(summary_folder) == True:
			os.system('rm -r %s' % summary_folder)
			os.system('mkdir %s' % summary_folder)
		else:
			os.system('mkdir %s' % summary_folder)

		for folder_name in folder_list:
			for index in range(1, data_splits + 1):
				file_name = '%s/%s.lmer.df.csv' % (folder_name, index)
				output_file = '%s/%s.ml.ready.txt' % (summary_folder, index)

				self.full_feature_selection_sub_function(file_name, output_file)

				file_name = '%s/%s.lmer.df.test.csv' % (folder_name, index)
				output_file = '%s/%s.ml.ready.test.txt' % (summary_folder, index)
				self.full_feature_selection_sub_function(file_name, output_file)

		print ("No feature selection with Done!")

	def full_feature_selection_sub_function(self, file_name, output_file):

		open_file = open(file_name,'r')
		file_readlines = open_file.readlines()

		output_txt = open(output_file,'w')

		for i in range(len(file_readlines)):
			read = file_readlines[i]
			read = read.replace(',','\t')

			if i == 0 or i == 4 or i > 4:
				output_txt.write(read)

		output_txt.close()
		open_file.close()

	#Feature selection
	#runned by R, mixed effect linear model (including random effects)
	def do_lmer(self, file_name, data_profile):
	
		if os.path.isdir(file_name) == True:
			os.system('rm -r %s' % file_name)
			os.system('mkdir %s' % file_name)
			out_dir = ('./%s' % file_name)
		else:
			os.system('mkdir %s' % file_name)
			out_dir = ('./%s' % file_name)

		print (file_name)
		os.system('Rscript ../../src/machine_learning_public/MLR_R_lmer.r %s %s' % (data_profile, out_dir))

	#Feature selection
	#After running the linear model, extract/summarize features from each iterations
	def extract_sig_features(self, file_name):
		cmd = 'ls %s/*.out > %s.out.list' % (file_name, file_name)
		os.system(cmd)
		out_list_file = '%s.out.list' % file_name
		out_list_readlines = open(out_list_file,'r').readlines()
		feature_selection_folder = '%s/feature_selection' % (file_name)

		if os.path.isdir(feature_selection_folder) == True:
			os.system('rm -r %s' % feature_selection_folder)
			os.system('mkdir %s' % feature_selection_folder)
		else:
			os.system('mkdir %s' % feature_selection_folder)

		for i in range(len(out_list_readlines)):
			ith_file = out_list_readlines[i]
			ith_file = ith_file.replace('\n','')

			ith_file_name = ith_file.split('/')[1]
			ith_output_txt = '%s/feature_selection/%s.sig.features' % (file_name,ith_file_name)
			ith_output_txt = open(ith_output_txt,'w')

			mlr_result_dict, chemID_list = LMFL.linear_model_result_manage(ith_file)
			for chemID in chemID_list:
				criteria = mlr_result_dict[chemID][0]
				if criteria == 3 or criteria == 2:
					ith_output_txt.write('%s\n' % chemID)
			ith_output_txt.close()

	def cv_ready_matrix_step_a(self, folder_list, summary_folder, data_splits):
	#Collects and summarizes significiant features
	#store them as files	

		summary_folder = '%s' % summary_folder

		if os.path.isdir(summary_folder) == True:
			os.system('rm -r %s' % summary_folder)
			os.system('mkdir %s' % summary_folder)
		else:
			os.system('mkdir %s' % summary_folder)

		for index in range(1, data_splits + 1):
			output_name = '%s/%s.list' % (summary_folder, index)
			for folder_name in folder_list:
				ith_data = '%s/feature_selection/%s.lmer.out.sig.features' % (folder_name, index)
				cmd = ('echo %s >> ./%s' % (ith_data, output_name))
				os.system(cmd)

	def cv_ready_matrix_step_b(self, folder_list, summary_folder, data_splits):
		#summary folder = folder that contains lists of path to sig features
		#i.list
		#folder_list = data folder
		#i.lmer.df.csv
		#i <= 64
		for index in range(1, data_splits + 1):
			ith_data_dict = {}# initialize every at every data split points
			ith_data_test_dict = {}# initialize every at every data split points

			feature_list_file = '%s/%s.list' % (summary_folder, index)
			feature_list_file =  open(feature_list_file,'r')
			feature_list_readlines = feature_list_file.readlines()

			#feature lists varies (1~4)
			for i in range(len(feature_list_readlines)):
				read = feature_list_readlines[i]
				ith_feature_file = read.replace('\n','')

				token = ith_feature_file.split('/')
				folder_name = token[0]

				ith_df_file = '%s/%s.lmer.df.csv' % (folder_name, index)
				ith_df_test_file = '%s/%s.lmer.df.test.csv' % (folder_name, index)

				ith_data_dict = self.cv_ready_matrix_step_b_submodule(ith_feature_file, ith_df_file, ith_data_dict)
				ith_data_test_dict = self.cv_ready_matrix_step_b_submodule(ith_feature_file, ith_df_test_file, ith_data_test_dict)

			self.write_ml_ready_matrix(ith_data_dict, summary_folder, index, '')
			self.write_ml_ready_matrix(ith_data_test_dict, summary_folder, index, '.test')


	def cv_ready_matrix_step_b_submodule(self, ith_feature_file, ith_df_file, ith_data_dict):

		ith_feature_file = open(ith_feature_file,'r')
		ith_feature_readlines = ith_feature_file.readlines()

		ith_df_file = open(ith_df_file,'r')
		ith_df_readlines = ith_df_file.readlines()

		sig_feature_list = ['das28','patientID']

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
				ith_data_dict['das28'] = token[1:]
			if i > 4:
				if token[0] in sig_feature_list:
					ith_data_dict[token[0]] = token[1:]

		ith_df_file.close()
		ith_feature_file.close()

		return ith_data_dict

	#Write text files that are ready for lmer.r
	def write_ml_ready_matrix(self, ith_data_dict, summary_folder, data_splits, label):

		file_dir = '%s/%s.ml.ready%s.txt' % (summary_folder, data_splits, label)
		output_txt = open(file_dir,'w')

		patientID_list = ith_data_dict['patientID']
		das28_list = ith_data_dict['das28']

		for patientID in patientID_list:
			if patientID != '':
				output_txt.write('\t%s' % patientID)
		output_txt.write('\n')

		output_txt.write('DAS28')
		for value in das28_list:
			if value != '':
				output_txt.write('\t%s' % value)
		output_txt.write('\n')

		for chemID in list(ith_data_dict.keys()):
			if chemID != 'patientID' and chemID != 'das28' and chemID != 'patient_dummyID':
				output_txt.write(chemID)
				value_list = ith_data_dict[chemID]
				for value in value_list:
					output_txt.write('\t%s' % value)
				output_txt.write('\n')
		output_txt.close()

if __name__ == "__main__":
	print ("Not meant to be run")
else:
	import os
	import sys
	import LINEAR_MODEL_FL as LMFL
	sys.path.insert(1, '../../src')

	print ("Loading MLFL_main")
