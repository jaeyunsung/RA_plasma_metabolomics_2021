#"create_SLM_plot_ready_profile.py"     19.12.31
#
#Because that MLM is difficult to interpret visually, I am trying to use SLM (that is also significant with the MLM) to draw a linear plot and color the data points by remission/no remission.
#If the idea or visualization seems promising, I might under go K-means clustering. Or, if it becomes complicated, EM clustering is my best bet
#
#
#

import sys
import os

if __name__ == "__main__":

	sys.path.insert(1, '/Users/m221138/RA_project/code')
	import LINEAR_MODEL_FL as LMFL
	import FL as FL

	data_profile_file = sys.argv[1]
	data_summarize_file = sys.argv[2]
	output_txt = sys.argv[3]
	output_txt = open('%s.profile.tsv' % output_txt, 'w')

	data_profile_dict, chemID_list, participantID_list = FL.data_profile_manage(data_profile_file)
	#data_profile_dict[chemID, participantID] = [participantID, chem_t1, chem_t2, fc_chem, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	summary_dict = LMFL.linear_model_summary_manage(data_summarize_file)

	FL.data_check(data_profile_file, chemID_list, participantID_list)

	dummy_chemID = str(chemID_list[0])
	for patientID in participantID_list:
		output_txt.write('\t%s_t1\t%s_t2' % (patientID, patientID))
	output_txt.write('\n')

	output_txt.write('DAS28')
	for patientID in participantID_list:
		info_list = data_profile_dict[dummy_chemID, patientID]
		das_t1 = info_list[4]
		das_t2 = info_list[5]
		output_txt.write('\t%s\t%s' % (das_t1, das_t2))
	output_txt.write('\n')

	output_txt.write('DAS_LABEL')
	for patientID in participantID_list:
		info_list = data_profile_dict[dummy_chemID, patientID]
		das_label = info_list[7]
		output_txt.write('\t%s\t%s' % (das_label, das_label))
	output_txt.write('\n')


	for chemID in summary_dict.keys():
		output_txt.write(str(chemID))
		chemID = str(chemID)

		for patientID in participantID_list:

			info_list = data_profile_dict[chemID, patientID]

			chem_t1 = info_list[1]
			chem_t2 = info_list[2]
			das_label = info_list[7]

			output_txt.write('\t%s\t%s' % (chem_t1, chem_t2))
		output_txt.write('\n')
			
	output_txt.close()



