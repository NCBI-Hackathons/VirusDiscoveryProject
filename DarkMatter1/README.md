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
JSON file of ORFS with names. 


### Slides
[Slides can be found HERE](https://docs.google.com/presentation/d/1eFzNYwwj6k5Wsn6cbxgObS9PiKS7d93hLxV40KVlwTo/edit#slide=id.g4d4d6c7cd0_0_15)

### Methods 
We will use jackhmmer to assign putatitive names to contigs that Team 5 passed to us. We will parse jackhmmer output and generate a JSON in the outlined format to team scaling. 

### Scripts and Parameters



### Contact

