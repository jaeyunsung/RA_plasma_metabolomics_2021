
import sys

chemID_profile_file = '../../../data/hd4_chemID_profile.txt'
chemID_profile_open = open(chemID_profile_file,'r')
chemID_profile_readlines = chemID_profile_open.readlines()

#meant to run with "MLR.clp.fac.ready.ignor.norm.qc.fillna.h.l.tsv.rm.error"
input_file = sys.argv[1]
input_open = open(input_file,'r')
input_readlines = input_open.readlines()

output_txt = open(sys.argv[2],'w')

chem_profile_dict = {}
#make chem_profile_dict
for i in range(len(chemID_profile_readlines)):
	read = chemID_profile_readlines[i]
	read = read.replace('\n','')
	read = read.replace('\r','')
	token = read.split('\t')
	chem_name = token[0]
	chemID = token[5]
	chem_profile_dict[chemID] = chem_name


for i in range(len(input_readlines)):
	read = input_readlines[i]

	if i == 0:
		output_txt.write(read)

	else:	
		read = read.replace('\n','')
		token = read.split('\t')
		chemID = token[0]
		chem_name = chem_profile_dict[chemID]
		
		output_txt.write('%s' % chem_name)
		for j in range(1, len(token)):
			output_txt.write('\t%s' % token[j])
		output_txt.write('\n')

output_txt.close()
