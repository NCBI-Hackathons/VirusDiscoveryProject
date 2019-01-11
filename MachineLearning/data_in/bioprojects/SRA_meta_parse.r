## download bioproject
#system('wget ftp://ftp.ncbi.nlm.nih.gov/bioproject/bioproject.xml')

require(XML)
data <- xmlParse("ftp://ftp.ncbi.nlm.nih.gov/bioproject/bioproject.xml")

xml_data <- xmlToList(data)

