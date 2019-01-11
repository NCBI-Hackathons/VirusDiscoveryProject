MAX = 1000000

data: get_contigs get_meta get_samples

big_data: get_big_contigs get_big_meta get_big_samples

get_contigs:
	bq query --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data limit 100" > contigs.json

get_big_contigs:
	bq query -n $(MAX) --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data" > big_contigs.json

get_meta:
	bq query --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select a.accession, a.contig, center, run_spots, run_bytes, run_bases, experiment, experiment_title, library_strategy, library_selection, library_source, library_layout, insert_size, insert_dev, platform, model, bio_project, study_name, study_title, sample, sample_type, bio_sample, sample_name, tax_id, scientific_name, common_name, display_name from hackathon.hackathon_data a join ( select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data limit 100) b on a.accession = b.accession and a.contig = b.contig" > metadata.json

get_big_meta:
	bq query -n $(MAX) --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select a.accession, a.contig, center, run_spots, run_bytes, run_bases, experiment, experiment_title, library_strategy, library_selection, library_source, library_layout, insert_size, insert_dev, platform, model, bio_project, study_name, study_title, sample, sample_type, bio_sample, sample_name, tax_id, scientific_name, common_name, display_name from hackathon.hackathon_data a join ( select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data limit $(MAX) ) b on a.accession = b.accession and a.contig = b.contig" > big_metadata.json

get_samples:
	bq query -n $(MAX) --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select a.accession, a.contig, sacc, btax, pident, evalue, bitscore, hit_len from hackathon.hackathon_data a join (select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data limit $(MAX) ) b on a.accession = b.accession and a.contig = b.contig" > known_samples.json

get_big_samples:
	bq query -n $(MAX) --format=json --project_id strides-sra-hackathon-data --nouse_legacy_sql "select a.accession, a.contig, sacc, btax, pident, evalue, bitscore, hit_len from hackathon.hackathon_data a join (select accession, contig, type, perc50, length, covered_length from hackathon.hackathon_data) b on a.accession = b.accession and a.contig = b.contig" > big_known_samples.json

meta:
	time ./loader.pl -c metadata -f metadata.json

contigs:
	time ./loader.pl -c contig -f contigs.json

samples:
	time ./loader.pl -c known_sample -f known_samples.json

flatten:
	./flatten.pl -d hackathon

load: meta contigs samples flatten

load_big_meta:
	time ./loader.pl -d big_hack -c metadata -f big_metadata.json

load_big_contigs:
	time ./loader.pl -d big_hack -c contig -f big_contigs.json

load_big_samples:
	time ./loader.pl -d big_hack -c known_sample -f big_known_samples.json

big_flatten:
	./flatten.pl -d big_hack

big_load: load_big_meta load_big_contigs load_big_samples big_flatten
