#!/usr/bin/python

import networkx as nx
import random,sys

# TYPE = 1 for scale free
TYPE = 1
SIZE = 1000
SEED = None
OUTPUT = 'networks/'
FILE = 'graph.out'

if __name__== '__main__':
	if len(sys.argv) == 2:
		TYPE = sys.argv[1]
	if len(sys.argv) == 3:
		SIZE = sys.argv[2]
	if len(sys.argv) == 4:
		SEED = sys.argv[3]

	if TYPE == 1:
		G = nx.barabasi_albert_graph(SIZE, 2, SEED)

	# Print to file
	f = open(OUTPUT+FILE, 'w')
	f.write(str(nx.number_of_nodes(G)) + '\n')
	edges = nx.edges(G)
	for e in edges:
		f.write('{} {}\n'.format(e[0],e[1]))
	
	f.close()