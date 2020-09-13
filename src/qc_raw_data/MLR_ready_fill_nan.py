#Designed to handle "MLR.clp.fac.ready.ignor.norm.qc.tsv" like data

import sys

input_file = sys.argv[1]
output_txt = input_file.split('.tsv')[1]
output_txt = '%s.fillna.tsv' % output_txt
output_txt = open(output_txt,'w')


input_file = open(input_file,'r')
input_readlines = input_file.readlines()

for i in range(len(input_readlines)):
	read = input_readlines[i]
	read = read.replace('\n','')

	if i <= 1:
		output_txt.write('%s\n' % read)
	else:
		token = read.split('\t')
		feature_name = token[0]
		feature_values = token[1:]
		feature_values_float_list = token[1:]

		if 'nan' in feature_values_float_list:
			feature_values_float_list.remove('nan')
		feature_values_float_list =[float(i) for i in feature_values_float_list]
		
		min_value = min(feature_values_float_list)

		output_txt.write(feature_name)
		for value in feature_values:
			if value == 'nan':
				output_txt.write('\t%s' % (float(min_value) / 2)) 
			else:
				output_txt.write('\t%s' % value)
		output_txt.write('\n')

output_txt.close()
