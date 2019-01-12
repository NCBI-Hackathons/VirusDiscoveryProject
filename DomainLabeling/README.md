# Domain Labeling using rpstblastn
Done:
Using full CDD database:
 - rpstblastn with e-value cut-off of 1e-3
 - output in JSON
 - split CDD database in :
    - Viral CDD --> Provided by Rodney 
    - Cellular CDD --> Provided by Rodney
    - Prokaryotic CDD --> Provided by Rodney 
    - mixed CDD

Pass-Fail strategy:
 - Fail = EU CDD > 3
 - Fail = PRO CDD > 3 && VIR CDD = 0

Tested (thanks Sam for filtering script):
 - Known-known:
 	- 10997 contigs
		- 8891 passed
		- 2975 have viral CDDs
		- 2416 are completely dark
 - Unknown-Unknown:
 	- 14614 contigs
		- 9625 passed
		- 711 have viral CDDs
		- 2525 completely dark
Running:
 - First complete testset from known (4 223 563 contigs)
	- 12 650 known known
	- 1836 known unknown
	- 4713 known unknown (50 - 85)
	- 4 204 364 unknown unknown
