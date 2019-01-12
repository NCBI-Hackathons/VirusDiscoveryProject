
# Scaling 
<p align="center"> *Metadata is the love letter to the future*  </p>
- we have no idea who said this but we are using it. 

The teams will be generating JSON files with metadata for each contig with its features which will be indexed using a database and joined accordingly to best address database lookups based on identified use cases. 

## Use cases supported with the indexes created 
- Datasets sourced from human gut: identified viruses,drilled down into known taxonomies and related families; and novel viruses
- Selected taxon (e.g., Human betaherpesviruses) and identification of all samples that contain that taxon
- Lookup datasets that have specific viral genes - e.g., capsid, tail fiber, helicase, reverse transcriptases, integrases, polymerases, proteases, etc.
- A user will want to know which runs contain reads that can be assembled into kind(s) (taxa/species) of virus and see wheather they correlate with reads that can be assembled into contigs of a particular: host taxa, environment integration of a particular known viruses from metagenomes in a certain part of Africa.
- Lookup all runs related to these models from samples in Germany with the words "pig silage" somewhere 

## Suggested JSON files realtionships
<p align="center">
  <img src="https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/ScalableIndex/hack.png?raw=true" alt="Table relationships"/>
</p>
  
## Benchmarking databases 

In order to make a conscious, educated decision about the schema, technology, and layout used for the organization of the data, several different solutions were proposed, prototyped and tested on different size of data to explore the scalability. The prototyped solutions tested included  - relational hierarchical database - PostgreSQL, 
- two schema-free solutions - SOLR, and MongoDB. 

The layout of the data that will be added to the database is anticipated to be  4 tables 
- SRA metadata, 
- contig description metadata, 
- known contigs information, and 
- unknown contig predictions. 

To improve usability, taxonomy and domain tables will need to be joined to the known and unknown contigs metadata. Some of the structured of the data was predicted to be more ameneable in a relational database structure as several unrelated data sets must be cross-referenced together for suporting all the listed use cases. 

###  Database Performance 
Query we tested - All the contigs that are: > 100 bp + associated with the University of Oxford + belong to “NC_019915”,

|               | Solr         | MongoDB     | PostgreSQL  |
| ------------- | ------------- |-------------|-------------|
| Query speed   | 1k- 0.1ms     |1k- 0.3s     | 1K - 0.3ms  |
|               | 1M - 60ms     |1M - 15s     | 1M - <2min  |
|Ease of search | has a defualt UI we used| command-line script used to lookup | UI possible but took some work |  
|Challeneges    | Took a while to learn how to serach in Solr UI | need to build a user interface  | performance and getting started| 

Although both Solr and MongoDB performed relatively well, we selected **MongoDB** based on the teams perference. 

We also tested MongoDB to run a query serach "lookup all contigs that have a certain length and retrieve all the contigs taxa information". This query was done to test if looking up multiple entries in the taxa field from the results will decrease the performance, also the taxa table had a different index compared to the other tables (shown below). MongoDB continued to performed really well (~1s) for these lookups. 

### PostgreSQL 
To setup PostgreSQL, here were the steps taken 
- Downloading and setting up PostsreSQL on VM 

- To import the JSON files to PostgreSQL databse, we used the script "JSON_to_Postgres.pl"
Indeed 

### MongoDb 
To setup MongoDB, the steps taken are written up under "mondodb" directory. Look at the readme here 

### Solr 
- Solr was setup on the VM from a docker image already, but this is a great resource to downlaod and get started with Solr http://www.solrtutorial.com/solr-in-5-minutes.html
Solr Admin GUI starts simultaenouly and most of the uploading and search was done using the interface. 

- Creating a core/collection on Solr 
./solr create -c blastdb #creating a core 
- Posting the JSON data to the core/collection  
./post -c blastdb ../../testdata/blastp.out.xml #indexing the xml or input JSON file 

To run the query for benchmarking the filters below were used on the known contigs table
- fq ={!join%20from=accession%20to=accession%20fromIndex=contigs}length:[100 TO * ]
  fq={!join%20from=accession%20to=accession%20fromIndex=metadata}center:UNIVERSITY OF OXFORD
- q=sacc:NC_019915

http://localhost:8983/solr/known_contigs/select?fq={!join%20from=accession%20to=accession%20fromIndex=contigs}length:[100%20TO%20*]&fq={!join%20from=accession%20to=accession%20fromIndex=metadata}center:UNIVERSITY%20OF%20OXFORD&q=sacc:NC_019915


## Presentation put toegther in hackathon and pre-hackathon ##
- Hackathon - https://docs.google.com/presentation/d/1qhToiEkrQo4-_BW6xScAQ0pzMXW-MufQ6dtQuhw9wVI/edit#slide=id.g4c3ef27744_0_127
- Pre-hackathon - https://docs.google.com/presentation/d/1ESJwy6Wkh6VH0SD-vVEA4gjVYbkh0R1ynuQ8E_ZoO_s/edit#slide=id.g4a4fdc18f9_25_40

## How we plan to scale all the data using MondoDB
<p align="center">
  <img src="logo2.png?raw=true" alt="Cookbook logo"/>
</p>

### Status of JSON files from all the teams, some of which were uploaded to the JSON_data directory
- SRA metadata - uploaded labelled as "bq-meta.zip"
- contigs table - 
- Taxonomy table - uploaded as "taxonomy.json"
- Annotation table - 
- known- 
- unknown -  

### Adding JSON files to MongoDB 
Currently because we are not working with all of SRA data, the files are being flattened to one big table instead of joining. Scaling up for this data will require joining, but for the current hackathon we were unable to explore the feasability. 

To flatten the file - run "flatten.pl" from mongodb 

### Lookup 
**API- Node JS**
- To lookup the data using command line, run query.pl in mongodb directory. 
- Using an API (node-js), goto 35.245.126.160/"write condition" 
  To get an idea of a few examples, we have a few conditions listed on the webpage "https://35.245.126.160
  The output is a reulting JSON file. 
- *Visualization* - the result from the API can be fed into a ipython notebook to generate some visulazation.
- Advantage- this does not need to be run from the same machine where MongoDB is setup

  More information is available under readme in virz/
  
**PyMongoDB**
- Needs to be setup on the same machine wher MongoDB was setup 
- Query search can be done using a Jupyter Notebooks, where the lookup commands can be done to retrieve soem fields. 
- Running on Jupyter Notebooks, with matplotlib libararies for visulaization 

An example script is available under virz/ry-test.ipynb.

## Things to consider for scalability ##
Currently this was all developed from the test data for 1 million entries. When we get real data from all the teams or all of SRA metadata, some of this may need to be changed but for now this works !! 
