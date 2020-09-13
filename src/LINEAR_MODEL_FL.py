def qc_lm_r_ready_file(data_file):

	data_file = open(data_file,'r')
	data_file_readlines = data_file.readlines()

	lm_ready_dict = {}
	lm_ignor_norm_dict = {}

	nan_rejected_chemID_list = []
	dist_rejected_chemID_list = []

	for i in range(len(data_file_readlines)):
		read = data_file_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		if i == 0:
			patientID_list = token[1:]
		if i <= 3 and i != 0:
			lm_ready_dict[token[0]] = token[1:]
			lm_ignor_norm_dict[token[0]] = token[1:]
		if i >= 4:
			chemID = token[0]
			value_list = token[1:]

			num_values = len(value_list)
			num_unique_value = len(list(set(value_list)))
			nan_rate = num_unique_value / num_values
			
			#Is it Gaussian?
			stat, p = shapiro(value_list)
			if p < 0.05:
				dist_rejected_chemID_list.append(chemID)

			#Too much nan? 
			if nan_rate < 0.8:
				nan_rejected_chemID_list.append(chemID)

			if p >= 0.05 and nan_rate >= 0.8:
				lm_ready_dict[chemID] = value_list
			if nan_rate >= 0.8:
				lm_ignor_norm_dict[chemID] = value_list

	return lm_ready_dict, lm_ignor_norm_dict, patientID_list, nan_rejected_chemID_list, dist_rejected_chemID_list

def list_to_text(data_list, data_file):

	output_txt = open(data_file,'w')
	for entry in data_list:
		output_txt.write('%s\n' % entry)
	output_txt.close()

def qc_control_results_to_text(data_dict, data_list, data_file):
	
	output_txt = open(data_file,'w')
	#intention : patienID_t1, patientID_t2 ...
	output_txt.write('patientID')
	for entry in data_list:
		output_txt.write('\t%s' % entry)
	output_txt.write('\n')
		
	for key in data_dict.keys():
		output_txt.write('%s' % key)
		value_list = data_dict[key]
		for value in value_list:
			output_txt.write('\t%s' % value)
		output_txt.write('\n')
	output_txt.close()

def linear_model_result_manage(data_file):

	data_dict = {}
	data_file_df = pd.read_csv(data_file, sep='\t', index_col=0)

	chemID_list = list(data_file_df.index)
	r, c = data_file_df.shape

	for i in range(r):
		lm_pval = data_file_df.iloc[i, 0]
		mlm_pval= data_file_df.iloc[i, 1]

		sex_sig = data_file_df.iloc[i, 2]
		age_sig = data_file_df.iloc[i, 3]

		if lm_pval != 'NaN' or mlm_pval != 'NaN':
			lm_pval = float(lm_pval)
			mlm_pval = float(mlm_pval)

			if lm_pval >= 0.05 and mlm_pval >= 0.05:
				criteria = 0
			if lm_pval < 0.05 and mlm_pval >= 0.05:
				criteria = 1
			if lm_pval > 0.05 and mlm_pval < 0.05:
				criteria = 2
			if lm_pval < 0.05 and mlm_pval < 0.05:
				criteria = 3
		
			data_dict[chemID_list[i]] = [criteria, lm_pval, mlm_pval, sex_sig, age_sig]

	return data_dict, chemID_list

def linear_model_summary_manage(data_file):

	data_dict = {}

	data_df = pd.read_csv(data_file, header=1, sep="\t", skiprows=0, index_col=0)
	r, c = data_df.shape

	for i in range(r):
		chemID = data_df.index.values[i]
		criteria = data_df.iloc[i,0]
		slm_pval = data_df.iloc[i,1]
		mvm_pval = data_df.iloc[i,2]

		if criteria == 3:
			data_dict[chemID] = [criteria, slm_pval, mvm_pval]

	return data_dict





if __name__ == '__main__':
	print ('This is Function library, do not run')

else:
	import pandas as pd
	from scipy.stats import shapiro
	print ("LOADING LINEAR_MODEL_FL")
