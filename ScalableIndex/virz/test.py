#!/usr/bin/env python3

import pandas as pd
import requests

def main():
    url = 'http://35.245.126.160/query?meta__scientific_name=/^human%20gut/'
    r = requests.get(url)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        print(df.head())

main()
