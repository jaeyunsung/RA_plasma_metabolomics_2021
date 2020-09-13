import sys
import os
sys.path.insert(1, '/Users/m221138/RA_project/code')
import FL
import LINEAR_MODEL_FL as LM


		
if __name__ == "__main__":

	data_file = sys.argv[1]
	lm_ready_dict, lm_ignor_norm_dict, patientID_list, nan_rejected_chemID_list, dist_rejected_chemID_list = LM.qc_lm_r_ready_file(data_file)

	result_output_txt = ('%s.qc.tsv' % data_file.split('.tsv')[0])
	result_summary_dir = ('%s.summary' % data_file.split('.tsv')[0])

	result_2_output_txt = ('%s.ignor.norm.qc.tsv' % data_file.split('.tsv')[0])

	if os.path.isfile(result_summary_dir) == True:
		os.system('rm -r %s' % result_summary_dir)
		os.system('mkdir %s' % result_summary_dir)
	else:
		os.system('mkdir %s' % result_summary_dir)

	dist_summary_output_txt = ('%s/%s.qc.dist.summary.tsv' % (result_summary_dir, data_file.split('.tsv')[0]))
	nan_summary_output_txt = ('%s/%s.qc.nan.summary.tsv' % (result_summary_dir, data_file.split('.tsv')[0]))

	LM.list_to_text(nan_rejected_chemID_list, nan_summary_output_txt)
	LM.list_to_text(dist_rejected_chemID_list, dist_summary_output_txt)
	LM.qc_control_results_to_text(lm_ready_dict, patientID_list, result_output_txt)
	LM.qc_control_results_to_text(lm_ignor_norm_dict, patientID_list, result_2_output_txt)

