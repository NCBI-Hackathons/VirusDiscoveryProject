
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
  <img src="https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/ScalableIndex/hack.png?raw=true" alt="Table relationships"/>
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

###  Database Performance 
Query we tested - All the contigs that are more than 100 bp and that were by University of Oxford, and belong to “NC_019915”,

|               | SOLR          | MongoDB     | PostgreSQL  |
| ------------- | ------------- |-------------|-------------|
| Query speed   | 1k- 0.1ms     |1k- 0.3s     | 1K - 0.3ms  |
|               | 1M - 60ms     |1M - 15s     | 1M - <2min  |
|Ease of search | has a defualt UI we used| command-line script used to lookup | UI possible but took some work |  
|Challeneges    | Took a while to learn how to serach in Solr UI | need to build a user interface  | performance and getting started| 

Although both SOLR and MongoDB performed relatively well, we selected **MongoDB** based on the teams perference. 

We also tested MongoDB to run a query serach "lookup all contigs that have a certain length and retrieve all the contigs taxa information". This query was done to test if looking up multiple entries in the taxa field from the results will decrease the performance, also the taxa table had a different index compared to the other tables (shown below). MongoDB continued to performed really well (~1s) for these lookups. 

### PostgreSQL 
To setup PostgreSQL, here were the steps taken 
- Downloading and setting up PostsreSQL on VM 

- To import the JSON files to PostgreSQL databse, we used the script "JSON_to_Postgres.pl"


### MongoDb 
To setup MongoDB, the steps taken are written up under "mondodb" directory. Look at the readme here 

### SOLR 
- SOLR was setup on the VM from a docker image already, but this is a great resource to downlaod and get started with SOLR http://www.solrtutorial.com/solr-in-5-minutes.html
SOLR UI starts simultaenouly and most of the uploading and search was done using the interface. 

- Creating a core/collection on SOLR 
./solr create -c blastdb #creating a core 
- Posting the JSON data to the core/collection  
./post -c blastdb ../../testdata/blastp.out.xml #indexing the xml or input JSON file 

To run the query for benchmarking, here are the fileter we used from the known contigs table
- fq ={!join%20from=accession%20to=accession%20fromIndex=contigs}length:[100 TO * ]
  fq={!join%20from=accession%20to=accession%20fromIndex=metadata}center:UNIVERSITY OF OXFORD
- q=sacc:NC_019915

http://localhost:8983/solr/known_contigs/select?fq={!join%20from=accession%20to=accession%20fromIndex=contigs}length:[100%20TO%20*]&fq={!join%20from=accession%20to=accession%20fromIndex=metadata}center:UNIVERSITY%20OF%20OXFORD&q=sacc:NC_019915


## Presentation put toegther in hackathon and pre-hackathon##
- Hackathon - https://docs.google.com/presentation/d/1qhToiEkrQo4-_BW6xScAQ0pzMXW-MufQ6dtQuhw9wVI/edit#slide=id.g4c3ef27744_0_127
- Pre-hackathon - https://docs.google.com/presentation/d/1ESJwy6Wkh6VH0SD-vVEA4gjVYbkh0R1ynuQ8E_ZoO_s/edit#slide=id.g4a4fdc18f9_25_40


## How we plan to scale all the data using MondoDB
<p align="center">
  <img src="logo2.png?raw=true" alt="Cookbook logo"/>
</p>

### Getting JSON files from all the teams 
- SRA metadata - SRA 
- contigs table - already assembled and table available from bigquery 
- Taxonomy table - 
- Annotation table - 
- known contigs table from Team 2
- 
