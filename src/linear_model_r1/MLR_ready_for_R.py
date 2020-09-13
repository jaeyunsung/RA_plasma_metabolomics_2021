import sys
import os
sys.path.insert(1, '/Users/m221138/RA_project/code')
import FL


def make_MLR_ready_text(output, data_profile_dict, simple_data_profile_dict, chemID_list, patientID_list):
	#STEP1 to create dataframe for MLR 
	#MLR: Multi Linear Regression
	#---------------
	#          Patient1_t1, Patient_1t2 ...
	#label
	#sex
	#age
	#DAS28
	#chemID 1
	#chemID 2
	#....
	#Dependent = chem
	#Independent = label, sex, age ETC
	for patientID in patientID_list:
		output.write('\t%s_t1\t%s_t2' % (patientID, patientID))
	output.write('\n')

	patient_count = 0
	output.write('patient_dummyID')
	for patientID in patientID_list:
		output.write('\t%s\t%s' % (patient_count, patient_count))
		patient_count = patient_count + 1
	output.write('\n')
	
	output.write('SEX')
	write_text(output, 'NA', data_profile_dict, simple_data_profile_dict, patientID_list, 5)
	output.write('AGE')
	write_text(output, 'NA', data_profile_dict, simple_data_profile_dict, patientID_list, 6)
	output.write('DAS')
	write_text(output, 'NA', data_profile_dict, simple_data_profile_dict, patientID_list, 1)
   
	for chemID in chemID_list:
		output.write(chemID)
		write_text(output, chemID, data_profile_dict, 'NA', patientID_list, 1)

def write_text(output, chemID, data_profile_dict, simple_data_profile_dict, patientID_list, index):

	#added 20.01.02
	if chemID == 'NA':
		if index == 5:
			for patientID in patientID_list:        
				value = simple_data_profile_dict[patientID][index]
				if value == 'female':
					value = 0
				if value == 'male':
					value = 1

				output.write('\t%s\t%s' % (value, value))
			output.write('\n')
		else:
			for patientID in patientID_list:        

				value_t1 = simple_data_profile_dict[patientID][index]
				value_t2 = simple_data_profile_dict[patientID][index + 1]

				output.write('\t%s\t%s' % (value_t1, value_t2))
			output.write('\n')

	else:
		
		for patientID in patientID_list:        

			try: value_t1 = data_profile_dict[chemID, patientID][index]
			except KeyError: value_t1 = "nan"

			try: value_t2 = data_profile_dict[chemID, patientID][index + 1]
			except KeyError: value_t2 = "nan"

			output.write('\t%s\t%s' % (value_t1, value_t2))
			
		output.write('\n')
		
if __name__ == "__main__":

	data_file = sys.argv[1]
	data_profile_dict, chemID_list, patientID_list = FL.data_profile_manage(data_file)
	patientID_list.sort()
	#data_profile_dict[chemID, participantID] = [participantID, chem_t1, chem_t2, fc_chem, das_t1, das_t2, fc_das, das_label,sex]
	simple_data_profile_dict, patientID_list_simple = FL.data_profile_manage_ver_simple(data_file)
	#data_profile_dict[participantID] = [participantID, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	patientID_list_simple.sort()

	output_txt = sys.argv[2]
	output_txt = open(output_txt,'w')

	make_MLR_ready_text(output_txt, data_profile_dict, simple_data_profile_dict, chemID_list, patientID_list)
	output_txt.close()


