#---------------	---------------- 19.12.23
import sys
import os

if __name__ == "__main__":

	sys.path.insert(1, '/Users/m221138/RA_project/code')
	import LINEAR_MODEL_FL as LMFL

	mlr_data_file = sys.argv[1]
	mlr_data_file_name = mlr_data_file.split('.tsv')[0]
	output_txt = open('%s.summarize.tsv' % mlr_data_file_name, 'w')

	mlr_result_dict, chemID_list = LMFL.linear_model_result_manage(mlr_data_file)
	#data_dict[chemID_list[i]] = [criteria, lm_pval, mlm_pval]

	output_txt.write('#Note criterea 0 = No significance, 1 = significance only in SLM, 2 = significance only in MLM, 3 = significance in both model \n')
	output_txt.write('%s\t%s\t%s\t%s\t%s\t%s\n' % ('chemID', 'criteria', 'lm_pval','mlm_pval', 'sex_sig', 'age_sig'))

	criteria_dict = {}

	for chemID in chemID_list:

		criteria = mlr_result_dict[chemID][0]
		lm_pval = mlr_result_dict[chemID][1]
		mlm_pval = mlr_result_dict[chemID][2]
		sex_sig = mlr_result_dict[chemID][3]
		age_sig = mlr_result_dict[chemID][4]

		if criteria not in criteria_dict.keys():
			criteria_dict[criteria] = 1
		else:
			criteria_dict[criteria] += 1

		output_txt.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (chemID, criteria, lm_pval, mlm_pval, sex_sig, age_sig))

	output_txt.close()
	
	print ('--------- statistics ----------')
	print ('data: %s' % mlr_data_file)
	print ('criteria | number of chemicals')
	for criteria in criteria_dict.keys():
		print ('%s : %s' % (criteria, criteria_dict[criteria]))
	print ('-------------------------------')

