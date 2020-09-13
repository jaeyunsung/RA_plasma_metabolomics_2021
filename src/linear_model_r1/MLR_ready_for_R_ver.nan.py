import sys
import os
sys.path.insert(1, '/Users/m221138/RA_project/code')
import FL

if __name__ == "__main__":

	data_file = sys.argv[1]
	data_profile_dict, chemID_list, patientID_list = FL.data_profile_manage(data_file)
	patientID_list.sort()
	#data_profile_dict[chemID, participantID] = [participantID, chem_t1, chem_t2, fc_chem, das_t1, das_t2, fc_das, das_label,sex]
	
	#simple_data_profile_dict, patientID_list_simple = FL.data_profile_manage_ver_simple(data_file)
	#data_profile_dict[participantID] = [participantID, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	#patientID_list_simple.sort()

	simple_dict = {}
	simple_patientID_list = []
	simple_chemID_list = []
	das_dict = {}

	for patientID in patientID_list:
		simple_patientID_list.append(patientID)

		for chemID in chemID_list:
			das_t1 = data_profile_dict[chemID, patientID][4]
			das_t2 = data_profile_dict[chemID, patientID][5]

			if das_t1 == 'nan':
				das = das_t2
				value = data_profile_dict[chemID,patientID][2]

			if das_t2 == 'nan':
				das = das_t1
				value = data_profile_dict[chemID,patientID][1]

			das_dict[patientID] = das
			simple_dict[chemID, patientID] = value

			if chemID not in simple_chemID_list:
				simple_chemID_list.append(chemID)
	
	simple_chemID_list.sort()
	simple_patientID_list.sort()

	output_txt = sys.argv[2]
	output_txt = open(output_txt,'w')

	output_txt.write('pateintID')
	for patientID in simple_patientID_list:
		output_txt.write('\t%s' % patientID)
	output_txt.write('\n')

	output_txt.write('DAS28')
	for patientID in simple_patientID_list:
		das_value = das_dict[patientID]
		output_txt.write('\t%s' % das_value)
	output_txt.write('\n')

	for chemID in simple_chemID_list:
		output_txt.write('%s' % chemID)
		for patientID in simple_patientID_list:
			value = simple_dict[chemID, patientID]
			output_txt.write('\t%s' % value)
		output_txt.write('\n')

	output_txt.close()


