
# Scaling 

The teams will be generating JSON files with metadata for each contig with its features which will be indexed using a database and joined accordingly to best adderess database lookups based on suggested use cases. 

## Use cases that should be addressed with the indexes 
- Datasets sourced from human gut, what virus types of present, broken down by known taxonomy, related families, and novel viruses?
- Select taxon (e.g., Human betaherpesviruses) and identify all samples that contain that taxon
- Lookup datasets that have specific viral genes - e.g., capsid, tail fiber, helicase, reverse transcriptases, integrases, polymerases, proteases, etc.
- A user will want to know which runs contain reads that can be assembled into some kind or kinds (taxa/species) of virus and see if they correlate with reads that can be assembled into contigs of a particular: host taxa, environment integration of a particular known viruses from metagenomes in a certain part of Africa.
- Lookup all runs related to these models from samples in germany with the words "pig silage" somewhere 

## Suggested JSON files realtionships
<p align="center">
< img src="https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/ScalableIndex/hack.png?raw=true" alt="Table relationships" /)
</p>
  
## Benchmarking databases 

In order to make a conscious, educated decision about the schema, technology, and layout used for the organization of the data, several different solutions were proposed and tested on different size of data to see which would work best at scale. The solutions tested included  - relational rigid hierarchical database - PostgreSQL, 
- two schema-free solutions - SOLR, and MongoDB. 

The layout of the data that will be added to the database is expected to be around 4 tables 
- SRA metadata, 
- contig description metadata, 
- known contigs information, and 
- unknown contig predictions. 

To add more usability, taxonomy and domain tables will need to be joined to the known and unknown contigs metadata. Some of the layout of the data was predicted to do better in a relational database structure as several unrelated data sets must be cross-referenced together in order to support queries. 



## Presentation ##

https://docs.google.com/presentation/d/1qhToiEkrQo4-_BW6xScAQ0pzMXW-MufQ6dtQuhw9wVI/edit#slide=id.g4c3ef27744_0_127
