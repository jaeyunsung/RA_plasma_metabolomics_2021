#
#analyze logistic regression results (Differential chemical abundance)
#


import sys

input_file_prefix = sys.argv[1]
condition_prefix = sys.argv[2]

condition_list = condition_prefix.split(',')
print (condition_list)

output_file = '%s.summary.tsv' % input_file_prefix
output_txt = open(output_file,'w')

for condition in condition_list:

	input_file = '%s.%s.tsv' % (input_file_prefix, condition)
	open_input_file = open(input_file,'r')
	input_file_readlines = open_input_file.readlines()

	output_txt.write('#%s\n' % condition)

	for i in range(len(input_file_readlines)):

		read = input_file_readlines[i]
		read = read.replace('\n','')
		token = read.split('\t')

		if i != 0:

			chemID = token[0]
			pval = token[1]

			if pval != 'error':
				if float(pval) <= 0.05:
					output_txt.write('%s\t%s\n' % (chemID, pval))
output_txt.close()

