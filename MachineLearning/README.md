# Machine Learning Team

## Objectives
- Assemble contig feature set: GC content, codon bias, information content, kmer frequency (GLOVE)
- Prediction of Virus Groups
- Prediction of % Dark Matter

## File Structure
```
MachineLearning/
+-- data_in/
|   +-- known_contigs.json
|   +-- known_contig_metadata.json
+-- feature_computed/
|   +-- contig_features.GLOVE.json
|   +-- contig_features.prodigal.json
|   +-- contif_features.TE_informatoin.json
+-- data_out/
|   +-- contig_features.all.json
+-- code
|   +-- taxID.py # convert tax ID to taxanomic groups
|   +-- feature_extraction/
|       +-- feature_extract.GLOVE.py
|       +-- feature_extract.prodigal.py
|       +-- feature_extract.TE_information.py
|   +-- predictors/
|       +-- training.viral_groups.py # random forest, ataboost, logit :: features.all --> taxanomic groups
|       +-- model.viral_groups.pickle
|       +-- run_model.viral_groups.py ## take contig and generate prediction
```
## To do list
[ ] get "known" contig set from #known team 
[ ] choose the taxanomic groups # taxID.py
[ ] generate contig_features.GLOVE.json
[ ] generate contig_features.prodical.json
[ ] generate contig_features.TE_informatoin.json
[ ] aggregate contig_features to .all
[ ] training.viral_groups.py 
[ ] run_model.viral_groups.py
