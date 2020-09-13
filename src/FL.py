def data_check(data_profile_file, chemID_list, participantID_list):

	print ('--------------------------------')
	print ('Data: %s' % data_profile_file)
	print ('#patients: %s' % len(participantID_list))
	print ('#Chemical IDs: %s' % len(chemID_list))
	print ('--------------------------------')


def treatment_profile_manage(data_file):

	open_data_profile = open(data_file,'r')
	data_profile_readlines = open_data_profile.readlines()
	data_profile_dict = {}

	treatment_list = []

	for i in range(len(data_profile_readlines)):

		read = data_profile_readlines[i]
		read = read.replace('\n','')
		token = read.split(',')

		if i == 0:

			for j in range(1, len(token)):
				treatment = token[j]
				treatment_list.append(treatment)

			print ('Total number of treatments: %s' % len(treatment_list))

		else:
			participantID = token[0]

			for j in range(1,len(token)):

				treatment_value = token[j]
				treatment_name = treatment_list[j-1]
				data_profile_dict[participantID, treatment_name] = int(treatment_value)

	return data_profile_dict, treatment_list

def data_profile_manage(data_file):

	open_data_profile = open(data_file,'r')
	data_profile_readlines = open_data_profile.readlines()
	data_profile_dict = {}
	chemID_list = []
	participantID_list = []

	for i in range(1, len(data_profile_readlines)):
		read = data_profile_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		chemID = token[0]
		chemID_list.append(chemID)

		participantID = token[1]

		chem_t1 = token[2]
		chem_t2 = token[3]

		fc_chem = token[4]
		age = token[5]

		age_t1 = age.split('/')[0]
		age_t2 = age.split('/')[1]

		sex = token[6]

		das_t1 = token[7].split('/')[0]
		das_t2 = token[7].split('/')[1]

		fc_das = token[8]
		das_label = token[9]

		participantID_list.append(participantID)
		data_profile_dict[chemID, participantID] = [participantID, chem_t1, chem_t2, fc_chem, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	
	chemID_list = list(set(chemID_list))
	participantID_list = list(set(participantID_list))

	return data_profile_dict, chemID_list, participantID_list


#currently not in use
def data_profile_manage_ver_simple(data_file):

	open_data_profile = open(data_file,'r')
	data_profile_readlines = open_data_profile.readlines()
	data_profile_dict = {}
	participantID_list = []

	for i in range(1, len(data_profile_readlines)):
		read = data_profile_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		participantID = token[1]

		age = token[5]

		age_t1 = age.split('/')[0]
		age_t2 = age.split('/')[1]

		sex = token[6]

		das_t1 = token[7].split('/')[0]
		das_t2 = token[7].split('/')[1]

		fc_das = token[8]
		das_label = token[9]

		participantID_list.append(participantID)
		data_profile_dict[participantID] = [participantID, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	
	participantID_list = list(set(participantID_list))

	return data_profile_dict, participantID_list



#currently not in use
def define_das_label_by_fc(das_t1, das_t2, cutoff):

	import math
	das_fc = math.log(das_t2/das_t1, 2)

	das_label = 0
	if das_fc > cutoff:
		das_label = 1
	if das_fc < -cutoff:
		das_label = -1
	
	return das_label

#currently not in use
def define_das_label_by_diff(das_diff):
	#das_diff = das_t1 - das_t2

	if das_diff > 1.2:
		label = -1
	if das_diff <= 1.2 and das_diff > 0.6:
		label = 0
	if das_diff <= 0.6:
		label = 1

	return label

#currently not in use
def define_das_label_by_absolute(das_diff):

	#das_diff = das_t2 - das_t1
	label = 'nan'
	if das_diff > 0:
		label = 1
	if das_diff < 0:
		label = 0

	return label

if __name__ == '__main__':
	print ('This is Function library, do not run')
else:
	print ("LOADING FL")
