library(lme4)
library(lmerTest)
library(stringr)
library(effects)

args <- commandArgs(trailingOnly=TRUE)
input_data <- args[1]
output_file <- args[2]

if (file.exists(output_file)){
    file.remove(output_file)
}

data_profile <- read.csv(input_data, sep="\t", row.names=1, header=TRUE)
data_profile <- as.data.frame(t(data_profile))

NUM_CHEM_ID <- ncol(data_profile)
NUM_patient_timepoint <- nrow(data_profile)

cat('chemID\tsimpleLRM_Fstatistics\tmultiLRM(chem_sig)\tmultiLRM(sex_sig)\tmultiLRM(age_sig)\n', file=output_file, append=TRUE)

for (i in 1:NUM_CHEM_ID){
    if (i > 4){
        output_string <- ''

        chemID <- colnames(data_profile)[i]
        chem_profile <- data_profile[,i]

        simple_LRM <- lm(DAS ~ chem_profile, data=data_profile)
        simple_LRM_stats <- summary(simple_LRM)$fstatistic

        simple_LRM_f_pvalue<- pf(simple_LRM_stats[1], simple_LRM_stats[2], simple_LRM_stats[3], lower.tail=FALSE)
        simple_LRM_rsquare <- summary(simple_LRM)$adj.r.squared

        multi_LRM <- lmer(DAS ~ chem_profile + SEX + AGE + (1|patient_dummyID), data=data_profile)

       	chem_sig <- anova(multi_LRM)$Pr[1]
        sex_sig <- anova(multi_LRM)$Pr[2]
        age_sig <- anova(multi_LRM)$Pr[3]

		output_string <- paste(chemID,"\t", simple_LRM_f_pvalue,"\t", chem_sig, "\t", sex_sig, "\t", age_sig, "\n")
		output_string <- str_replace_all(output_string, " ", "")
        cat(output_string, file=output_file, append=TRUE)
    }
}
print ("END MLR_R_lmer.r")

