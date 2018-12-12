# README

## Synopsis

contains 'viral specific' CDD's, parsed based on viral_keywords.txt
cddid.tbl parsed with:

'''
cut -f1,2,3 cddid.tbl | grep -i -f viral_keywords.txt > virus_spec_CDD.tbl
'''
