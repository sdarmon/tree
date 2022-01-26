from ete3 import Tree
from os import walk
import numpy as np
import sys
import threading

def leaf_name(node):
	"""
	Input: A node (or tree)
	Output: The list of the name of all leaves under that node (or tree)
	"""
	return([leaf.name for leaf in node])

def inter(L,L2):
	"""
	Input: Two lists or sets
	Output: The list of intersected elements
	"""
	S = []
	for l in L2:
		if l in L:
			S.append(l)
	return(S)

def nb_seq(t):
	nb = 0 
	for seq in leaf_name(t):
		if seq[:3] == "TRA" or seq[:3] == "APA":
			nb += 1
	return(nb)

def comptInduction(t):
	"""
	Input: t a tree
	Output : R : the list of valid trees (i.e. trees that contain exactly one quadra)
			 [AD,MU,MM,MA] : the count of each type of sequence
	"""
	if t.is_leaf():
		if t.name[:3] == "APA" or t.name[:3] == "TRA":
			typ = t.name[3:5]
			if  typ == "AD":
				return([],[1,0,0,0])
			elif typ == "MU":
				return([],[0,1,0,0])
			elif typ == "MM":
				return([],[0,0,1,0])
			elif typ == "MA":
				return([],[0,0,0,1])
			else:
				return([],[0,0,0,0])

		else:
			return([],[0,0,0,0])
	AD = 0
	MU = 0
	MM = 0
	MA = 0
	R = []
	QuadraInSon = 0
	for fils in t.children:
		R2,L= comptInduction(fils)
		ad,mu,mm,ma = L
		R = R+R2
		AD+=ad
		MU+=mu
		MM+=mm
		MA+=ma
		if ad == 1 and mu == 1 and mm == 1 and ma == 1 :
			QuadraInSon = 1
	if not(QuadraInSon) and AD == 1 and MU == 1 and MM == 1 and MA == 1 :
		R.append(t)
	return(R,[AD,MU,MM,MA])


def splitTree(t):
	"""
	Input: t a tree
	Output: Two lists of trees. The first one is the list of tree that contains exactly one quadra
			The other one contains t if it is invalid (not the good amonts of quadra)
	"""
	R,Quadra = comptInduction(t)
	ad,mu,mm,ma = Quadra
	r = len(R)
	if r == 0 and ad+mu+mm+ma == 0:
		return([],[],[t])
	elif r == ad and r == mu and r == mm and r == ma :
		return(R,[],[])
	else:
		return([],[t],[])


def loading(path):
	"""
	Input: The path to the dirctory containing the data
	Output: n : the numbers of data; trees : every loaded tree; leaf_names : the list of the name of the leaves for each tree.
	"""
	filenames = next(walk(path), (None, None, []))[2]  #Getting the name of every file in the directory data
	RegTrees = []
	ErrTrees = []
	EmpTrees = []
	for file in filenames:
		t = Tree(path+file) #Loading tree
		nb = nb_seq(t)
		R,E,M = splitTree(t)
		if R!= []:
			RegTrees.append([file]+R[:])
		if E != []:
			ErrTrees.append([file]+E[:])
		if M != []:
			EmpTrees.append([file]+M[:])
	return(RegTrees,ErrTrees,EmpTrees)

def sub_tree(t):
	"""
	Input: t a tree
	Output: the same tree, whitout any useless branches, but it can remain useless node
	"""
	if t.is_leaf():
		if t.name[:3] == "APA" or t.name[:3] == "TRA":
			return(t)
		else : 
			return(None)
	else:
		L = t.children
		inducL = [sub_tree(l) for l in L]
		inducL = [el for el in inducL if el != None]
		if inducL == []:
			return(None)
		else:
			t2 = Tree()
			for T in inducL:
				t2.add_child(T)
			return(t2)

def max_dist(t,subtree):
	"""
	Input: t an original tree and subtree, one of its embedded subtree.
	Output: d+1 with d is the minimum number of branches that have to be remove the get the subtree as an induced subtree of t.
	"""
	leaves = leaf_name(subtree)
	m = 0
	for leaf in leaves:
		for leaf2 in leaves:
			if leaf != leaf2:
					m = max(m,t.get_distance(leaf,leaf2, topology_only=True))
	return(int(m)-2)



def simplification_tree(t):
	"""
	Input: t a tree
	Output: t2 a tree where every useless node have been removed.
	"""
	if t.is_leaf():
		return(t)
	elif len(t.children) == 1:
		t2 = simplification_tree(t.children[0])
		return(t2)
	else:
		t2 = Tree()
		for T in t.children:
			t2.add_child(simplification_tree(T))
		return(t2)

def type_quadra(t,i):
	"""
	Input: t a tree and i the d computed by the function max_dist
	Output: The type of the tree t
	"""
	if len(t.children) == 2 :
		a,b = t.children
		if b.is_leaf and b.name[3:5] == "MA":
			if len(a.children) == 2:
				c,d = a.children
				if d.is_leaf and d.name[3:5] == "MM":
					if len(c.children) == 2:
						e,f = c.children
						if (e.name[3:5] == "AD" and f.name[3:5] == "MU") or (f.name[3:5] == "AD" and e.name[3:5] == "MU") :
							return(i)
				elif c.is_leaf and c.name[3:5] == "MM":
					if len(d.children) == 2:
						e,f = d.children
						if (e.name[3:5] == "AD" and f.name[3:5] == "MU") or (f.name[3:5] == "AD" and e.name[3:5] == "MU") :
							return(i)
		elif a.is_leaf and a.name[3:5] == "MA":
			if len(b.children) == 2:
				c,d = b.children
				if d.is_leaf and d.name[3:5] == "MM":
					if len(c.children) == 2:
						e,f = c.children
						if (e.name[3:5] == "AD" and f.name[3:5] == "MU") or (f.name[3:5] == "AD" and e.name[3:5] == "MU") :
							return(i)
				elif c.is_leaf and c.name[3:5] == "MM":
					if len(d.children) == 2:
						e,f = d.children
						if (e.name[3:5] == "AD" and f.name[3:5] == "MU") or (f.name[3:5] == "AD" and e.name[3:5] == "MU") :
							return(i)
	return(-i)


def processing(path_directory,mode):
	"""
	Input: A path to a directory and mode, the mode of writing in files
	Output: Nothing
	"""
	RegTrees,ErrTrees,EmpTrees = loading(path_directory)
	comptDist = []
	comptType = []
	nb_quadra = 0
	err = 0
	with open('output.txt',mode) as f:
		for L in RegTrees:
			file = L[0][:-15]
			trees = L[1:]
			quadras = []
			types = []
			for t in trees:
				tree = sub_tree(t)
				dist = max_dist(t,tree)
				if dist > 1 :
					comptDist.append(file)
				tree = simplification_tree(tree)
				quadras.append(tree)
				types.append(type_quadra(tree,dist))
				nb_quadra+=1
			S = file
			for dist in types:
				if dist != 1:
					comptType.append(file)
				S = S+"\t"+str(dist)
			for tree in quadras:
				S = S+"\t"+tree.write()
			f.write(S)
			f.write('\n')
	with open('outputErr.txt',mode) as f:
		for L in ErrTrees:
			file = L[0][:-15]
			trees = L[1:]
			quadras = []
			types = []
			for t in trees:
				tree= sub_tree(t)
				nb = nb_seq(t)
				quadras.append(simplification_tree(tree))
				types.append(nb)
				err+=1
			S = file
			for dist in types:
				S = S+"\t"+str(dist)
			for tree in quadras:
				S = S+"\t"+tree.write()
			f.write(S)
			f.write('\n')
	with open('outputEmp.txt',mode) as f:
		for L in EmpTrees:
			file = L[0][:-15]
			f.write(file)
			f.write('\n')
	print("\n", nb_quadra, "valid quadruplets have been found over",len(RegTrees), "trees and they have been stored in the file output.txt .\n")
	print("\n There are", err, "non-valid trees (stored in the file outputErr.txt) and", len(EmpTrees),"empty trees (stored in the file outputEmp.txt).\n")
	print("\nThere are",len(comptDist), "valid quadruplet(s) which aren't induced sub-tree(s) (",comptDist,")\n")
	print("\nThere are",len(comptType), "valid quadruplet(s) which aren't organized according to the sequence AD,MU,MM,MA (",comptType,")\n")
	return(None)

def showing(argu,i):
	t = Tree(argu)
	print(t)
	return(None)


def start():
	"""
	Input : Nothing
	Output : Start the computation according to what the user want.
			 One can type the following command :
			  -"python3 tree.py file" with "file" a name of a tree to print it in the console (the extention ".ReconciledTree" not mandatory)
			  -"python3 tree.py file -s" to show the tree in an graphic interface
			  -"python3 tree.py file -q" to show the quadruplet(s) of the tree in the console
			  -"python3 tree.py file -sq" to show the quadruplet(s) of the tree in an graphic interface (if there are more than 2, they will be shown one by one)
			  -"python3 tree.py directory" to find the quadruplets of the trees inside the directory
			  -"python3 tree.py directory -a" to complete the files output.txt, outputErr.txt and outputEmp.txt with new trees of a directory
	"""
	Arg = sys.argv[1:]
	if len(Arg) == 1 and Arg[0][-1] != '/': #Case file
		file = Arg[0]
		if len(file) >15 and file[-15:] == ".ReconciledTree":
			print(Tree(file))
		else:
			print(Tree(file+".ReconciledTree"))
	elif len(Arg) == 1 and Arg[0][-1] == '/': #Case path
		processing(Arg[0],'w')
	elif len(Arg) == 2 and Arg[0][-1] == '/' and  Arg[1] == "-a": #Case path and add
		processing(Arg[0],'a')
	elif len(Arg) == 2 and Arg[0][-1] != '/' and  Arg[1] == "-s": #Case file and show
		file = Arg[0]
		if len(file) >15 and file[-15:] == ".ReconciledTree":
			t = Tree(file)
		else:
			t = Tree(file+".ReconciledTree")
		t.show()
	elif len(Arg) == 2 and Arg[0][-1] != '/' and  Arg[1] == "-q": #Case file and show quadruplet
		file = Arg[0]
		if len(file) >15 and file[-15:] == ".ReconciledTree":
			t = Tree(file)
		else:
			t = Tree(file+".ReconciledTree")
		R,E,M = splitTree(t)
		if R == []:
			print("Warning: this tree hasn't any valid quadruplets")
		for t2 in R:
			print(simplification_tree(sub_tree(t2)))
	elif len(Arg) == 2 and Arg[0][-1] != '/' and  Arg[1] == "-sq" or Arg[1] == "-qs": #Case file and show quadruplet
		file = Arg[0]
		if len(file) >15 and file[-15:] == ".ReconciledTree":
			t = Tree(file)
		else:
			t = Tree(file+".ReconciledTree")
		R,E,M = splitTree(t)
		if R == []:
			print("Warning: this tree hasn't any valid quadruplets")
		for t2 in R:
			t2=simplification_tree(sub_tree(t2))
			t2.show()
	else:
		print("Wrong arguments given in input.")

start()