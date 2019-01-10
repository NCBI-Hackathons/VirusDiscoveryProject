# Product Testing

## Example VIGA Command Call
* Requires database consisting of BLAST formatted RefSeq Virus, DIAMOND formatted RefSeq Virus, INFERNAL compressed Rfam, and PVOG HMMs
* Database can be provided by #testing group

`./run-viga --input ERR2538396.known_knowns1.fasta --diamonddb /data/databases/RefSeq_Viral_DIAMOND/refseq_viral_proteins.dmnd --blastdb /data/databases/RefSeq_Viral_BLAST/refseq_viral_proteins.faa --rfamdb /data/databases/rfam/Rfam.cm --hmmerdb /data/databases/pvogs/pvogs.hmm --modifiers modifiers.txt`

### Shortcomings
* Explicit locations are required for all databases, even those you do not want to use OR that current VIGA version does not use
* Annotates against known viral databases only - could be modified to include all of RefSeq or other HMM databases but will increase run time
* Renumbers input contig IDs to VIGA specific IDs - but order is maintained


## Testing Use Cases:

### Filter queries categorically
Users want to filter which results are returned based on relevant metadata associated with an SRA dataset. For example:
- Search by: Environment, Dataset size, Host organisms, Location of sample, and basically any other SRA metadata field
- Example question #1 - Datasets sourced from 'human gut', what virus types of present, broken down by known taxonomy, related families, and novel viruses?
- Example question #2 - Select a subset of datasets all sourced from 'Africa', what virus types of present, broken down by known taxonomy, related families, and novel viruses?
- Example application - Integration of a particular known or all novel viruses from metagenomes from a specified geographical region.

### Querying a virus type and identify all datasets that contain it
- Select taxon (e.g., Human betaherpesviruses) and identify all samples that contain that taxon
- Identify all runs which contain reads corresponding to this taxon

### Query an input virus and find n% similar viruses across all datasets by ANI (or k-mer match)
- From there: ability to access the original files for subsequent downstream analysis: genomic comparison, phylogenetic trees
- For matches - capacity to filter by sample type 
- Example application - Profile viral diversity 
- Example inquiry - Search for all runs with contigs with similarity to query sequence/input virus.

### Filtering for virus output for various categories
- Have access to all decision points in the index - what thresholds were met to achieve categorization?
- Possible to identify viruses that are predicted to be circularized or near-complete based on nearest neighbors?
- Information regarding predicted ORFs and information on coding vs. non-coding status?
- Ability to filter based on coverage depth threshold, with/without reference guide.

### Searching for proteins with specific functions - viral and auxiliary metabolic genes
- Interest for viral genes - e.g., capsid, tail fiber, helicase, reverse transcriptases, integrases, polymerases, proteases, etc.
- Interest for AMGs - previous examples include: PSII in cyanophages, drug-resistance cassettes, nitrate reductases, etc.
- Stretch: Being able to access those sequences for downstream analysis

### Host Identification
- For taxon that have known virus match - known hosts
- Potential hosts based on protein structure/function
- Hosts of closely related viruses
- Viruses of closely related hosts
