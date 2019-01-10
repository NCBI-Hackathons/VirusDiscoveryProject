## Dark Matter 1 
![](http://vignette4.wikia.nocookie.net/callofduty/images/7/79/Dark_Matter_Camouflage_menu_icon_BO3.png/revision/latest?cb=20160506200857)

_Jan Buchmann, Cody Glickman, Laura Milena, Forero Junco, Lindsay Rutter, Ryan Shean_

### Objective
Collating output of multiple teams to identify novel viral contigs in metagenomic datasets

### Overview
```
/intact/
 |
 +-- input  \\ From genes
 |
 +-- output \\ To DarkMatter2
```

### Internal JSON data
```
{
  domains: [
            {start: int, end: int,name: char},
            {start: int, end: int,name: char}
            ],
  orfs: [
          {start: int, end: int,name: char},
          {start: int, end: int,name: char}
        ]
}
```
### Required Tools


### Expected Input


### Projected Output
JSON file of our decorations to team scaling

### Methods
Take output from #genes group and count number of open reading frames and number of domains. If we have at least two domains with hits we keep the contig and if not we pass to group 7. 

We will use jackhmmer to find putative annotations for all open reading frames. 
### Scripts and Parameters



### Contact

