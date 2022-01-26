# Quadruplets in Tree

The goal of this project is to find particular quadruplet of sequences in phylogenetic trees.


## Data 


The data used is phylogenetic trees. There are Newick Tree and each leaf of each tree matchs with an unique genetic sequence. There are three types of sequences :
* ENS... : Correspond to original sequences of the phylogenetic tree (which can be found at https://www.ensembl.org/index.html )
* TRA... and ADA... : Sequences added in the pylogenetic tree by the research team. Then, these sequences are divided into four additional species :
	+ AD... : Spiny mouse (Acomys Dimidiatus)
	+ MU... : Mouse Gerbil (Meriones Unguiculatus)
	+ MM... : Mouse (Mus Minutoides) 
	+ MA... : Hamster (Mesocricetus Auratus)



## Objective

Each genetic sequence of the four species is replaced in the phylogenetic tree and the goal of this project is to study how they are related to each other, i.e. for each gene, what kind of phylogenetic tree they are forming. The following tree is an example extract from the data for the gene sequence `ENSGT00390000006707` :

<img src="image/Example1.png" width="50%">
