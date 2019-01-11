library(SRAdb)
# (down)load SRA
sqlfile <- "/home/bkellman/VirusDiscoveryProject/MachineLearning/data_in/SRAdb/SRAmetadb.sqlite" 
if( !file.exists(sqlfile)){
	sqlfile <- getSRAdbFile()
}

# connect to db
sra_con <- dbConnect(SQLite(),sqlfile)

# get tables
sra_tables <- dbListTables(sra_con)

# load all SRR ids
srr = as.character(read.table('../allSRR.txt')[[1]])

# query
i=0
#rs <- dbGetQuery(sra_con,'select study_abstract from study where study_accession is "SRR2992957"')
rs=do.call(rbind,lapply(srr,function(x){
 #i=i+1
 print(x)
 #print(paste(i,'/',length(srr)))
 dbGetQuery(sra_con,paste0("select * from study INNER JOIN run ON study.submission_accession=run.submission_accession where run.run_accession is '",
	x,"'")) 
}))

write.csv(rs,file='SRA.sel_SRR_all.csv')

