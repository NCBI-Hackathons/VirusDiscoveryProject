# Clustering and Phylogeny
This part of the ViralDiscoveryProject aims to answer the question: **How are these new contigs related to known viruses and each other**?

## 'Simple' Clustering
The goal of this section is to provide the simplest answer to users who are searching through the database, find a putative virus they're interested in, and wonder: "Are there any similar contigs?" 

Each contig will be assigned to a single cluster, and each cluster will be represented by one "representative contig".  Often times a contig will be the "representative contig" in its own cluster. We colloquially refer to these as 'lonely contigs'.

| Cluster Representative Sequence | Sequence in Cluster |
|----------------------------------------|--------------------------------------------------------|
| NC_027054_Porcine_kobuvirus | NC_027054_Porcine_kobuvirus |
| NC_027054_Porcine_kobuvirus | NC_011829_Porcine_kobuvirus_swine/S-1-HUN/2007/Hungary |
| NC_027054_Porcine_kobuvirus | NC_016769_Porcine_kobuvirus_SH-W-CHN/2010/China |
| NC_018226_Pasivirus_A1 | NC_018226_Pasivirus_A1 |
| NC_016156_Feline_picornavirus | NC_016156_Feline_picornavirus |
| NC_001479_Encephalomyocarditis_virus | NC_001479_Encephalomyocarditis_virus |
| NC_010810_Human_TMEV-like_cardiovirus | NC_010810_Human_TMEV-like_cardiovirus |
| NC_010810_Human_TMEV-like_cardiovirus | NC_009448_Saffold_virus |
| NC_038306_Coxsackievirus_A2 | NC_038306_Coxsackievirus_A2 |
| NC_015936_Mouse_kobuvirus_M-5/USA/2010 | NC_015936_Mouse_kobuvirus_M-5/USA/2010 |
| NC_022332_Eel_picornavirus_1 | NC_022332_Eel_picornavirus_1 |
| NC_024765_Chicken_picornavirus_1 | NC_024765_Chicken_picornavirus_1 |
| NC_024765_Chicken_picornavirus_1 | NC_028380_Chicken_sicinivirus_JSY |
| NC_024768_Chicken_picornavirus_4 | NC_024768_Chicken_picornavirus_4 |
| NC_024768_Chicken_picornavirus_4 | NC_023858_Melegrivirus_A |
| NC_024768_Chicken_picornavirus_4 | NC_021201_Turkey_hepatitis_virus_2993D |


## Full Clustering
Here we aim to cluster all contigs and all refseq viruses (again) but extract actual edge weights between the nodes in the cluster. This will be done using blastn and extracting the SECOND top hit (the top hit will be the virus matching to itself). If a virus has no second hits, it's 'lonely' and wont show up to the graph.

