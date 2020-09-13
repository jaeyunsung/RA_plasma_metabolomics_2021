#DAM_to_VolcanoPlot.r					20.03.20
#hur.benjamin@mayo.edu
#
#Drawing Volcano Plots for RA project
#
#cmd: Rscript DEG_to_VolcanoPlot.r [input] [output_prefix]

library(ggplot2)
library(ggrepel)

#test dataset

args <- commandArgs(trailingOnly=TRUE)
input_file = read.csv(args[1], sep="\t", header=TRUE)
output_prefix = args[2]

chem_mean_1 <- input_file[,3]
chem_mean_2 <- input_file[,4]
#fc <- chem_mean_1 / chem_mean_2
fc <- chem_mean_2 / chem_mean_1
input_file$log2FoldChange <- log2(fc)

#defining new dataframe
x_axis <- input_file$log2FoldChange
y_axis <- -log10(input_file$pval)
#gene_list <- rownames(input_file)
gene_list <- input_file$chemID
df <- do.call(rbind, Map(data.frame, 'log2FC'=x_axis, 'pvalue'=y_axis))
rownames(df) <- gene_list
df$genes <- row.names(df)

#Thresholds for data points color

#pvalue 0.05 = 1.30103 (-10logpvalue)
sig_subset <- subset(df, pvalue > 1.30103)
sig_red_subset <- subset(sig_subset, log2FC > 0)

print ("up")
print (sig_red_subset[1])
print (nrow(sig_red_subset))
sig_blue_subset <- subset(sig_subset, log2FC < 0)
print ("down")
print (sig_blue_subset[1])
print (nrow(sig_blue_subset))

#Plot for labels
output_pdf_label <- paste(output_prefix, ".label.pdf", sep="")
pdf(output_pdf_label)

ggplot(df, aes(x=log2FC, y=pvalue))+ coord_cartesian(xlim=c(-2,2), ylim=c(0,3))+ geom_point(colour="grey") +
geom_point(data = sig_red_subset, colour="red") +
geom_point(data = sig_blue_subset, colour="blue") +
geom_text_repel(data=sig_red_subset, aes(log2FC, pvalue, label=genes), colour="red", size=2) +
geom_text_repel(data=sig_blue_subset, aes(log2FC, pvalue, label=genes), colour="blue", size=2) +
ylab("-log10 (P-value)")
dev.off()

#Plot without labels
output_pdf_label <- paste(output_prefix, ".nolabel.pdf", sep="")
pdf(output_pdf_label)
ggplot(df, aes(x=log2FC, y=pvalue))+ coord_cartesian(xlim=c(-2,2), ylim=c(0,3))+ geom_point(colour="grey") +
geom_point(data = sig_red_subset, colour="red") +
geom_point(data = sig_blue_subset, colour="blue") +
ylab("-log10 (P-value)")
dev.off()



