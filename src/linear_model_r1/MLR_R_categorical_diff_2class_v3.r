library(lme4)
library(lmerTest)
library(effects)
library(stringr)

run_glmer <- function(main_df){
	model = glmer(label ~ chem_abundance + sex + scale(age) + (1|dummyID/visit), data = main_df, family = binomial)
	pval_list = coef(summary(model))[,4]
	pval = pval_list[2]

	if (pval == 0){
		pval <- "error"
	}
	return (pval)
}

args <- commandArgs(trailingOnly = TRUE)
output_dir <- args[1]
file_prefix <- args[2]

data_dir <- "/Users/m221138/RA_plasma_metabolites/analysis/differential_abundance_v4/2class_v2/"
data_category_list <- c("rl.v2.tsv", "mh.v2.tsv")

#I HATE NON-ZEROBASED LIST INDEX
NUM_CATEGORY <- length(data_category_list) + 1

counter <- 1
counter_2nd <- counter + 1


while (counter < NUM_CATEGORY){
#Outer Category Loop

	category_1 <- data_category_list[counter]
	category_1 <- strsplit(category_1,".tsv")

	print ("file 1")
	file_name_1 <- paste(data_dir, file_prefix, '.',category_1, ".tsv", sep="")

	log_message <- paste("STEP #", counter, sep="")
	print (log_message)
	log_message <- paste("= ", file_name_1, sep="")
	print (log_message)

	counter_2nd <- counter + 1
	
	while (counter_2nd < NUM_CATEGORY){
	#Inner Category Loop
		category_2 <- data_category_list[counter_2nd]
		category_2 <- strsplit(category_2, ".tsv")

		print ("file 2")
		file_name_2 <- paste(data_dir, file_prefix, '.',category_2, ".tsv", sep="")
		print (file_name_2)
		print ('hello')
		log_message <- paste("=== ", file_name_2, sep="")
		print (log_message)

		print ("output txt")
		output_txt = paste(output_dir, '/', file_prefix, '.rl.mh.tsv', sep="")
		print (output_txt)
		if (file.exists(output_txt)){
			file.remove(output_txt)
		}

		output_string <- paste("chemID\tpval\t",file_name_1,"\t", file_name_2,"\n", sep="")
		cat(output_string, file=output_txt, append=TRUE)
	   
		data_df_1 <- read.csv(file_name_1, sep="\t", header=TRUE, row.names=1)
		data_df_1 <- as.data.frame(t(data_df_1))
		NUM_CHEM_ID_1 <- ncol(data_df_1)
		NUM_PATIENTS_1 <- nrow(data_df_1)
		
	   	print ('2')
		data_df_2 <- read.csv(file_name_2, sep="\t", header=TRUE, row.names=1)
		data_df_2 <- as.data.frame(t(data_df_2))
		NUM_CHEM_ID_2 <- ncol(data_df_2) 
		NUM_PATIENTS_2 <- nrow(data_df_2)
	
		chemID_list <- colnames(data_df_1)
		chemID_list_2 <- colnames(data_df_2)
		
		if (identical(chemID_list, chemID_list_2) != TRUE){
		#Error Check
			print ("Error, Two given files have different size")
		}
		if (NUM_CHEM_ID_1 == NUM_CHEM_ID_2){
		#Start integrate two files    
			for (i in 1:NUM_CHEM_ID_1){
				if (i > 5){
					
					#START: Create analysis ready dataframe
					#col = dummyID, sex, age, DAS28, label
					chem_column_ID <- chemID_list[i]
					debug_log <- paste(i, chem_column_ID)
					#print (debug_log)
					
					temp_df_1 <- data_df_1[,1:5]
					label_1 <- rep(1:1, each=NUM_PATIENTS_1)
					chem_value_list_1 <- data_df_1[,i]
					mean_chem_1 <- mean(chem_value_list_1)

					temp_df_1$label <- label_1 
					temp_df_1$chem_abundance <- chem_value_list_1
				
					temp_df_2 <- data_df_2[,1:5]
					label_2 <- rep(0:0, each=NUM_PATIENTS_2)
					chem_value_list_2 <- data_df_2[,i]
					mean_chem_2 <- mean(chem_value_list_2)

					temp_df_2$label <- label_2
					temp_df_2$chem_abundance <- chem_value_list_2
				

					main_df <- rbind(temp_df_1, temp_df_2)
					#END: Create analysis ready dataframe


					pval <- tryCatch(run_glmer(main_df), error = function(e){ return ("error")})

					output_string <- paste(chem_column_ID,"\t",pval,"\t",mean_chem_1,"\t", mean_chem_2,"\n", sep="")
					cat(output_string, file=output_txt,append=TRUE)
				}
			}
		}    
	counter_2nd <- counter_2nd + 1
	}
	counter <- counter + 1
}
