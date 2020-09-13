#!/usr/bin/env python
# coding: utf-8
#19.12.05.  #converted from "create_table.ipynb" 

# In[46]:
import sys
import numpy
import pandas as pd
from scipy.stats import pearsonr
import math


# In[47]:
def add_key_to_dict(input_dict, input_reverse_dict, key, value):
    
    input_reverse_dict[str(value)] = key
    
    if key in input_dict.keys():
        if len(input_dict[key]) <= 1:
            input_dict[key].append(value)
        else:
            print("CAUTION: More than 2 time point for this patient! ")
            
    if key not in input_dict.keys():
        input_dict[key] = [value]
        
    return input_dict, input_reverse_dict

def add_profile_to_dict(input_1_dict, input_2_dict, participant_id, age, sex, das):

	if participant_id in input_2_dict.keys():
		input_2_dict[participant_id][0] = ('%s/%s'% (input_2_dict[participant_id][0], age))
		input_2_dict[participant_id][1] = ('%s/%s'% (input_2_dict[participant_id][1], sex))
		input_2_dict[participant_id][2] = ('%s/%s'% (input_2_dict[participant_id][2], das))

	if participant_id not in input_2_dict.keys():
		try :
			sample_ids = ('%s/%s' % (input_1_dict[participant_id][0], input_1_dict[participant_id][1]))
		except KeyError:
			sample_ids = 'NA'

		input_2_dict[participant_id] = [str(age), str(sex), str(das), sample_ids]

	return input_2_dict


if __name__ == "__main__":

	sys.path.insert(1, '../code')
	import FL

#input directory
	input_dir = '../data/'
	table_file = sys.argv[1]
	output_name = sys.argv[2]
#output
	output_file_dir = ('%s%s' % (input_dir, output_name))

#Patient Meta: Making dataframe that contains patient informations
	patient_info_1_file = input_dir + 'accrual_report_hd4.csv' #sample ID -- external_patient_ID
	patient_info_1_df = pd.read_csv(patient_info_1_file, dtype=object)
	patient_info_1_df = patient_info_1_df.iloc[:,[0,9]]
	patient_info_1_df = patient_info_1_df.rename(columns={"External Participant Id" : "External_Participant_Id"})

	patient_info_2_file = input_dir + 'RA_biobank_2019June17_sheet1.csv' ##external_patient_ID -- age sex
	patient_info_2_df = pd.read_csv(patient_info_2_file)
	patient_info_2_df = patient_info_2_df.iloc[:,[0,4,5,6]]

	patient_info_1_dict = {}  #key = external participant id , value = sample id
	patient_info_r_1_dict = {} #key = sample id,  value = external participant id 
	patient_info_2_dict = {}  #other patients profile

	for i in range(len(patient_info_1_df)):
		sample_id = patient_info_1_df.iloc[i,0]
		participant_id = patient_info_1_df.iloc[i,1]
		patient_info_1_dict, patient_info_r_1_dict = add_key_to_dict(patient_info_1_dict, patient_info_r_1_dict, participant_id, sample_id)


	for i in range(len(patient_info_2_df)):
		participant_id = patient_info_2_df.iloc[i,0]
		age = patient_info_2_df.iloc[i,1]
		sex = patient_info_2_df.iloc[i,2]
		das = patient_info_2_df.iloc[i,3]
		
		patient_info_2_dict = add_profile_to_dict(patient_info_1_dict, patient_info_2_dict, participant_id, age, sex, das)

#Completed patient profiling. will be saved after including time series data.
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#Obtaining list for CLIENT IDENTIFIER
	open_table_file = open(table_file,'r')
	table_file_readlines = open_table_file.readlines()

	client_id_list = table_file_readlines[0].replace('\n','').split(',')
	client_id_list = client_id_list[3:]
	open_table_file.close()

	print (int(len(client_id_list)/2), " of patients")

	data_table = pd.read_csv(table_file, dtype=object, skiprows=8)
	chemID_list = data_table.iloc[:,1] #entry varies

	time_series_matrix = data_table.iloc[:,3:]
	N_ROW_TIME_SERIES_MATRIX, N_COLUMN_TIME_SERIES_MATRIX = time_series_matrix.shape

	TEMP_MAX_COUNT = N_COLUMN_TIME_SERIES_MATRIX

	output_file = open(output_file_dir,'w')

#Considerable note so far.
#patient_info_1_dict = {}  #key = external participant id , value = sample id
#patient_info_r_1_dict = {} #key = sample id,  value = external participant id 
#patient_info_2_dict = {}  #other patients profile : [age, sex, das, sample_id_alpha/sample_id_beta]
#client_id_list = [] #client id lists from hd4_scaled data

#writing header of the output file
	output_file.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' 
					  % ('chemID', 'participantID','chem_T1','chem_T2','FC(log2)','age','sex','DAS', 'DAS_diff', 'DAS_label'))

	clientID_error_list = []

	for i in range(len(chemID_list)): 
	#i <= varies
		chemID = chemID_list[i]
		TEMP_COUNT = 0
		while TEMP_COUNT < TEMP_MAX_COUNT:
		#0 ~ 152 patient number
		
			ALPHA = float(time_series_matrix.iloc[i,TEMP_COUNT])
			BETA = float(time_series_matrix.iloc[i,TEMP_COUNT +1])
			client_identifier_alpha = client_id_list[TEMP_COUNT]
			client_identifier_beta = client_id_list[TEMP_COUNT + 1]
			
			FC = math.log(BETA/ALPHA, 2)
			
			try :
				if patient_info_r_1_dict[client_identifier_alpha] == patient_info_r_1_dict[client_identifier_beta]:
					participant_id = patient_info_r_1_dict[client_identifier_alpha]
				else:
					print ("Somthing wrong between the relationship of client identifer alpha ~ beta")
			except KeyError:
				participant_id = patient_info_r_1_dict[client_identifier_beta]

				if client_identifier_beta not in clientID_error_list:
					print ("Note that client identifier is missing : %s, %s" % (client_identifier_alpha, client_identifier_beta))
					clientID_error_list.append(client_identifier_beta)
				
			age = patient_info_2_dict[participant_id][0]
			sex = patient_info_2_dict[participant_id][1].split('/')[0]                
			das = patient_info_2_dict[participant_id][2]
			das_t1 = float(das.split('/')[0]) 
			das_t2 = float(das.split('/')[1]) 

			das_diff = das_t2 - das_t1
			label = FL.define_das_label_by_absolute(das_diff)

			#might have to do a loop if its getting bigger.......
			output_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (chemID, participant_id, ALPHA, BETA, FC, age, sex, das, das_diff, label))
			TEMP_COUNT += 2

	output_file.close()

