#!/usr/bin/env python3

# Author: Ken Youens-Clark <kyclark@email.arizona.edu>
# Purpose: Demonstrate how to get data from Virz into Python

import pandas as pd
import requests

def main():
    #url = 'http://35.245.126.160/query?meta__scientific_name=/^human%20gut/'
    url = 'http://35.245.126.160/query?meta__bio_project=PRJEB24383'
    r = requests.get(url)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        df.drop(columns=['_id'], inplace=True)
        print(df.head())

main()
