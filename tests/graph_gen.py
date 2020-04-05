# -*- coding: utf-8 -*-

import networkx as nx

class GraphGenerator:
    EdgeNames = ['F', 'D', 'P', 'E', 'H', 'K',
                 'C', 'S', 'O', 'L', 'R', 'T', 'X', 'Z']
    EdgeProbs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def __init__(self):
        self.G = nx.MultiGraph()
        self.G.graph['edge_names'] = self.EdgeNames
        self.G.graph['edge_probs'] = self.EdgeProbs
        
        
    def as_multigraph(self):
        return self.G

    def as_one_graph(self):
        return nx.Graph(self.G)

    def as_dict_of_graphs(self):
        Graphs = {}
        i = 0
        for l in self.EdgeNames:
            FG = nx.Graph()
            FG.graph['edge_name'] = l
            FG.graph['edge_prob'] = self.G.graph['edge_probs'][i]
            FG.add_nodes_from(self.G)
            selected_edges = [(u, v, e) for u, v, e in self.G.edges(
                data=True) if e['label'] == l]
            FG.add_edges_from(selected_edges)
            Graphs[l] = FG
            i = i + 1
        return Graphs

    def print_multi(self):
        dot_G = nx.nx_pydot.to_pydot(self.G)
        print(dot_G)

    def draw_multi(self, filename='raj.png'):
        A = nx.nx_agraph.to_agraph(self.G)
        A.layout('dot')
        A.draw(filename)