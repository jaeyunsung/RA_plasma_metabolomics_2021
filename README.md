Plasma Metabolomic Profiling in Patients with Rheumatoid Arthritis Identifies Biochemical Features Indicative of Quantitative Disease Activity
=========================

DOI : TBD

Benjamin Hur, Vinod K. Gupta, Harvey Huang, Kerry A. Wright, Kenneth J. Warrington, Veena Taneja, John M. Davis III, and Jaeyun Sung

Contact: hur.benjamin@mayo.edu
Corresponding Author : sung.jaeyun@mayo.edu


##### 1. Differentially Abundant metabolites

>src/linear_model_r1/MLR_R_categorical_diff_2class_v2.r

>analysis/differential_abundance_public/2class/run.sh

##### 2. Feature selection for quantitative disease activity of RA

>src/machine_learning_public/All_IN_ONE_FeatureSelection_CV_LOO.py

>analysis/selection_scheme_public/run.sh

##### 3. Other statistics

Investigation of drugs (csDMARD, TNFi-bDMARD, non-TNFi-bDMARD, MTX, PRED) that affected the abundance of metabolites.
>src/statistics/drug_effect_lmer_R.ipynb

Differentially abundant metabolites related test. 
Investigates whether confounding effects (drug, smoke, age, etc) differs between higher and lower disease activity.
>src/statistics/ftest_comfounds.ipynb

Investigation of prescription (csDMARD, TNFi-bDMARD, non-TNFi-bDMARD, MTX, PRED) differences between visit 1 and visit 2.
>code/statistics/mcnemar_test_R.ipynb


#### DATA

preprocessed data: Training datset (n=128)
>data/discovery_cohort

preprocessed data: Test dataset (n=12)
>data/validation_cohort

