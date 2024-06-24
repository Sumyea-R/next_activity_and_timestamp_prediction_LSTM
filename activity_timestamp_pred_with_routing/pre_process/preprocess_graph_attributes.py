import networkx as nx
import regex as re

'''
Sample Usage
> import preprocess_graph_attributes as preprocess_graph
> processed_LG_nw = preprocess_graph.preprocess_graph_attributes(path_to_file+'logistic-network.gml')
Returns logistic network with deserialised edge and node attributes 
'''

def preprocess_edge_attributes(G=nx.DiGraph):
	for edge in G.edges():
		if G[edge[0]][edge[1]]['score'] != '{(-1, -1, -1, -1, -1, -1)}':
			data = G[edge[0]][edge[1]]['score']
			data = data.replace('{','')
			data = data.replace('}','')

			str_tuples = re.findall(r'\(.*?\)', data)
			score_set = set()
			for item in str_tuples:
				values_str = re.findall(r'[0-9A-Z]+', item)
				converted_tuple = tuple([values_str[0], # src-area
							 values_str[1], # dst-area
							 int(values_str[2]), # score
							 values_str[3], # curr
							 values_str[4], # next
							 int(values_str[5])]) #isn
				score_set.add(converted_tuple)

			G[edge[0]][edge[1]].update(score=score_set)

		else:
			G[edge[0]][edge[1]].update(score={(-1,-1,-1,-1,-1,-1)})


def preprocess_node_attributes(G:nx.DiGraph):
	for node in G.nodes():
		if G.nodes[node].get('src_eqt_loc'):
			data = G.nodes[node]['src_eqt_loc']
			data = data.replace('{','')
			data = data.replace('}','')

			str_tuples = re.findall(r'\(.*?\)', data)
			loc_pair_set = set()
			for item in str_tuples:
				values_str = re.findall(r'[0-9A-Z]+', item)
				if len(values_str)==2:
					converted_tuple = tuple([values_str[0], values_str[1]])
					loc_pair_set.add(converted_tuple)

			G.nodes[node].update(src_eqt_loc=loc_pair_set)

		if G.nodes[node].get('dst_eqt_loc'):
			data = G.nodes[node]['dst_eqt_loc']
			# print(type(data), data)
			data = data.replace('{','')
			data = data.replace('}','')

			str_tuples = re.findall(r'\(.*?\)', data)
			loc_pair_set = set()
			for item in str_tuples:
				values_str = re.findall(r'[0-9A-Z]+', item)
				if len(values_str)==2:
					converted_tuple = tuple([values_str[0], values_str[1]])
					loc_pair_set.add(converted_tuple)

			G.nodes[node].update(dst_eqt_loc=loc_pair_set)
			

def preprocess_graph_attributes(path_to_nw_file:str):
	'''
    Input: NetworkX gml file 
    Returns: deserialised DiGraph object
    '''
	logistic_nw = nx.read_gml(path_to_nw_file)
	preprocess_edge_attributes(logistic_nw)
	print('Processed edge attribute: \'score\'')

	preprocess_node_attributes(logistic_nw)
	print('Processed node attributes: \'src_eqt_loc\' and \'dst_eqt_loc\'')

	return logistic_nw