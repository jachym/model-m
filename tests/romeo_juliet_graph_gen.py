# from graphviz import Graph
import networkx as nx


class RomeoAndJuliet:
    EdgeNames = ['F', 'D', 'P', 'E', 'H', 'K',
                 'C', 'S', 'O', 'L', 'R', 'T', 'X', 'Z']
    EdgeProbs = [0.9, 0.8, 0.9, 0.8, 0.7, 0.9, 1, 0.7, 0.5, 0.9, 0.9, 0.5, 0.3, 0.7]

    def __init__(self):

        self.G = nx.MultiGraph()
        self.G.graph['edge_names'] = self.EdgeNames
        self.G.graph['edge_probs'] = self.EdgeProbs
        

        # Romeo and Juliet
        self.G.add_node(1, label='Romeo', sex=0, age=18)
        self.G.add_node(2, label='Juliet', sex=1, age=13)
        self.G.add_edge(1, 2, label='F')

        # House of Montague
        self.G.add_node(3, label='Lord Montague', sex=0, age=58)
        self.G.add_node(4, label='Lady Montague', sex=1, age=40)
        self.G.add_edge(3, 4, label='F')
        self.G.add_edge(3, 1, label='F')
        self.G.add_edge(4, 1, label='F')
        self.G.add_edge(3, 4, label='D')
        self.G.add_edge(3, 1, label='D')
        self.G.add_edge(4, 1, label='D')
        self.G.add_node(5, label='Benvolio', sex=0, age=17)
        self.G.add_edge(1, 5, label='F')
        self.G.add_edge(3, 5, label='F')
        self.G.add_edge(4, 5, label='F')

        # House of Capulet
        self.G.add_node(6, label='Lord Capulet', sex=0, age=50)
        self.G.add_node(7, label='Lady Capulet', sex=1, age=35)
        self.G.add_edge(2, 6, label='F')
        self.G.add_edge(2, 7, label='F')
        self.G.add_edge(6, 7, label='F')
        self.G.add_edge(2, 6, label='D')
        self.G.add_edge(2, 7, label='D')
        self.G.add_edge(6, 7, label='D')
        self.G.add_node(8, label='Tybalt', sex=0, age=17)
        self.G.add_edge(8, 2, label='F')
        self.G.add_edge(8, 6, label='F')
        self.G.add_edge(8, 7, label='F')
        self.G.add_edge(8, 2, label='D')
        self.G.add_edge(8, 6, label='D')
        self.G.add_edge(8, 7, label='D')

        # House of Prince of Verona
        self.G.add_node(9, label='Prince Escalus', sex=0, age=60)
        self.G.add_node(10, label='Paris', sex=0, age=24)
        self.G.add_node(11, label='Mercutio', sex=0, age=20)
        self.G.add_edge(9, 10, label='F')
        self.G.add_edge(9, 10, label='D')
        self.G.add_edge(9, 11, label='F')
        self.G.add_edge(10, 11, label='F')
        self.G.add_edge(1, 11, label='Z')

        # Servants
        self.G.add_node(12, label='Nurse', sex=1, age=28)
        self.G.add_edge(2, 12, label='P')
        self.G.add_edge(2, 12, label='D')
        self.G.add_edge(2, 6, label='D')
        self.G.add_edge(2, 7, label='D')
        self.G.add_edge(2, 8, label='D')
        self.G.add_node(13, label='Peter', sex=0, age=60)
        self.G.add_edge(13, 12, label='P')
        self.G.add_edge(13, 12, label='D')
        self.G.add_edge(13, 6, label='D')
        self.G.add_edge(13, 7, label='D')
        self.G.add_edge(13, 1, label='D')
        self.G.add_edge(13, 8, label='D')
        self.G.add_node(14, label='Balthasar', sex=0, age=23)
        self.G.add_edge(1, 14, label='P')
        self.G.add_edge(1, 14, label='Z')
        self.G.add_edge(1, 14, label='D')
        self.G.add_edge(14, 3, label='D')
        self.G.add_edge(14, 4, label='D')
        self.G.add_node(15, label='Abram', sex=0, age=68)
        self.G.add_edge(3, 15, label='P')
        self.G.add_edge(4, 15, label='P')
        self.G.add_edge(3, 15, label='D')
        self.G.add_edge(4, 15, label='D')
        self.G.add_edge(1, 15, label='D')
        self.G.add_edge(14, 15, label='D')
        self.G.add_node(16, label='self.Gregory', sex=0, age=34)
        self.G.add_node(17, label='Sampson', sex=0, age=36)
        self.G.add_edge(6, 16, label='P')
        self.G.add_edge(7, 16, label='P')
        self.G.add_edge(8, 16, label='P')
        self.G.add_edge(8, 17, label='P')
        self.G.add_edge(6, 17, label='P')
        self.G.add_edge(7, 17, label='P')
        self.G.add_edge(8, 16, label='Z')
        self.G.add_edge(8, 17, label='Z')
        self.G.add_node(18, label='Page', sex=0, age=11)
        self.G.add_edge(18, 10, label='P')
        self.G.add_edge(18, 10, label='D')

        # Friars and Merchants
        self.G.add_node(19, label='Friar Lawrence', sex=0, age=68)
        self.G.add_node(20, label='Friar John', sex=0, age=42)
        self.G.add_edge(19, 20, label='P')
        self.G.add_edge(19, 1, label='C')
        self.G.add_edge(19, 2, label='C')
        self.G.add_edge(19, 20, label='C')
        self.G.add_node(21, label='Apothacary', sex=0, age=75)
        self.G.add_edge(21, 1, label='O')
        self.G.add_edge(21, 2, label='O')

        # Former love interest of Romeo
        self.G.add_node(22, label='Rosaline', sex=1, age=16)
        self.G.add_edge(1, 22, label='Z')

        # Fairy Quenn Mab visits Romeo in a dream
        self.G.add_node(23, label='Queen Mab', sex=1, age=20)
        self.G.add_edge(1, 23, label='T')

        # self.Grandpa Capulet
        self.G.add_node(24, label='Old Capulet', sex=0, age=82)
        self.G.add_edge(24, 2, label='F')
        self.G.add_edge(24, 6, label='F')
        self.G.add_edge(24, 7, label='F')
        self.G.add_edge(24, 8, label='F')

        # Capulets Servants
        self.G.add_node(25, label='Anthony', sex=0, age=38)
        self.G.add_node(26, label='Potpan', sex=0, age=35)
        self.G.add_node(27, label='Servant 1', sex=0, age=49)
        self.G.add_node(28, label='Servant 2', sex=0, age=31)
        self.G.add_edge(6, 25, label='P')
        self.G.add_edge(6, 26, label='P')
        self.G.add_edge(6, 27, label='P')
        self.G.add_edge(6, 28, label='P')
        self.G.add_edge(7, 25, label='P')
        self.G.add_edge(7, 26, label='P')
        self.G.add_edge(7, 27, label='P')
        self.G.add_edge(7, 28, label='P')

        # Petruchio is a ghost at Capulet party
        self.G.add_node(29, label='self.Ghost Petruchio', sex=0, age=27)
        self.G.add_edge(2, 29, label='T')

        # Valentine is Mercutio brother at a party
        self.G.add_node(30, label='Valentine', sex=0, age=26)
        self.G.add_edge(9, 30, label='F')
        self.G.add_edge(10, 30, label='F')
        self.G.add_edge(11, 30, label='F')

        # Watchmen at a fight
        self.G.add_node(31, label='Watchmen 1', sex=0, age=29)
        self.G.add_node(32, label='Watchmen 2', sex=0, age=25)
        self.G.add_node(33, label='Watchmen 3', sex=0, age=30)
        self.G.add_edge(31, 32, label='P')
        self.G.add_edge(31, 33, label='P')
        self.G.add_edge(33, 32, label='P')

        # Musicians at a party
        self.G.add_node(34, label='Musician 1', sex=0, age=39)
        self.G.add_node(35, label='Musician 2', sex=0, age=31)
        self.G.add_node(36, label='Musician 3', sex=0, age=49)
        self.G.add_edge(34, 35, label='P')
        self.G.add_edge(34, 36, label='P')
        self.G.add_edge(35, 36, label='P')

        # One-man chorus
        self.G.add_node(37, label='Chorus', sex=0, age=61)

        # party at Capulet - is now a complete subgraph
        self.G.add_edge(1, 5, label='K')
        self.G.add_edge(1, 6, label='K')
        self.G.add_edge(1, 7, label='K')
        self.G.add_edge(1, 8, label='K')
        self.G.add_edge(1, 9, label='K')
        self.G.add_edge(1, 10, label='K')
        self.G.add_edge(1, 11, label='K')
        self.G.add_edge(1, 16, label='K')
        self.G.add_edge(1, 17, label='K')
        self.G.add_edge(1, 22, label='K')
        self.G.add_edge(1, 25, label='K')
        self.G.add_edge(1, 26, label='K')
        self.G.add_edge(1, 27, label='K')
        self.G.add_edge(1, 28, label='K')
        self.G.add_edge(1, 29, label='K')
        self.G.add_edge(1, 34, label='K')
        self.G.add_edge(1, 35, label='K')
        self.G.add_edge(1, 36, label='K')

        self.G.add_edge(5, 6, label='K')
        self.G.add_edge(5, 7, label='K')
        self.G.add_edge(5, 8, label='K')
        self.G.add_edge(5, 9, label='K')
        self.G.add_edge(5, 10, label='K')
        self.G.add_edge(5, 11, label='K')
        self.G.add_edge(5, 16, label='K')
        self.G.add_edge(5, 17, label='K')
        self.G.add_edge(5, 22, label='K')
        self.G.add_edge(5, 25, label='K')
        self.G.add_edge(5, 26, label='K')
        self.G.add_edge(5, 27, label='K')
        self.G.add_edge(5, 28, label='K')
        self.G.add_edge(5, 29, label='K')
        self.G.add_edge(5, 34, label='K')
        self.G.add_edge(5, 35, label='K')
        self.G.add_edge(5, 36, label='K')

        self.G.add_edge(6, 7, label='K')
        self.G.add_edge(6, 8, label='K')
        self.G.add_edge(6, 8, label='K')
        self.G.add_edge(6, 10, label='K')
        self.G.add_edge(6, 11, label='K')
        self.G.add_edge(6, 16, label='K')
        self.G.add_edge(6, 17, label='K')
        self.G.add_edge(6, 22, label='K')
        self.G.add_edge(6, 25, label='K')
        self.G.add_edge(6, 26, label='K')
        self.G.add_edge(6, 27, label='K')
        self.G.add_edge(6, 28, label='K')
        self.G.add_edge(6, 29, label='K')
        self.G.add_edge(6, 34, label='K')
        self.G.add_edge(6, 35, label='K')
        self.G.add_edge(6, 36, label='K')

        self.G.add_edge(7, 8, label='K')
        self.G.add_edge(7, 9, label='K')
        self.G.add_edge(7, 10, label='K')
        self.G.add_edge(7, 11, label='K')
        self.G.add_edge(7, 16, label='K')
        self.G.add_edge(7, 17, label='K')
        self.G.add_edge(7, 22, label='K')
        self.G.add_edge(7, 25, label='K')
        self.G.add_edge(7, 26, label='K')
        self.G.add_edge(7, 27, label='K')
        self.G.add_edge(7, 28, label='K')
        self.G.add_edge(7, 29, label='K')
        self.G.add_edge(7, 34, label='K')
        self.G.add_edge(7, 35, label='K')
        self.G.add_edge(7, 36, label='K')

        self.G.add_edge(8, 9, label='K')
        self.G.add_edge(8, 10, label='K')
        self.G.add_edge(8, 11, label='K')
        self.G.add_edge(8, 16, label='K')
        self.G.add_edge(8, 17, label='K')
        self.G.add_edge(8, 22, label='K')
        self.G.add_edge(8, 25, label='K')
        self.G.add_edge(8, 26, label='K')
        self.G.add_edge(8, 27, label='K')
        self.G.add_edge(8, 28, label='K')
        self.G.add_edge(8, 29, label='K')
        self.G.add_edge(8, 34, label='K')
        self.G.add_edge(8, 35, label='K')
        self.G.add_edge(8, 36, label='K')

        self.G.add_edge(9, 10, label='K')
        self.G.add_edge(9, 11, label='K')
        self.G.add_edge(9, 16, label='K')
        self.G.add_edge(9, 17, label='K')
        self.G.add_edge(9, 22, label='K')
        self.G.add_edge(9, 25, label='K')
        self.G.add_edge(9, 26, label='K')
        self.G.add_edge(9, 27, label='K')
        self.G.add_edge(9, 28, label='K')
        self.G.add_edge(9, 29, label='K')
        self.G.add_edge(9, 34, label='K')
        self.G.add_edge(9, 35, label='K')
        self.G.add_edge(9, 36, label='K')

        self.G.add_edge(10, 11, label='K')
        self.G.add_edge(10, 16, label='K')
        self.G.add_edge(10, 17, label='K')
        self.G.add_edge(10, 22, label='K')
        self.G.add_edge(10, 25, label='K')
        self.G.add_edge(10, 26, label='K')
        self.G.add_edge(10, 27, label='K')
        self.G.add_edge(10, 28, label='K')
        self.G.add_edge(10, 29, label='K')
        self.G.add_edge(10, 34, label='K')
        self.G.add_edge(10, 35, label='K')
        self.G.add_edge(10, 36, label='K')

        self.G.add_edge(11, 16, label='K')
        self.G.add_edge(11, 17, label='K')
        self.G.add_edge(11, 22, label='K')
        self.G.add_edge(11, 25, label='K')
        self.G.add_edge(11, 26, label='K')
        self.G.add_edge(11, 27, label='K')
        self.G.add_edge(11, 28, label='K')
        self.G.add_edge(11, 29, label='K')
        self.G.add_edge(11, 34, label='K')
        self.G.add_edge(11, 35, label='K')
        self.G.add_edge(11, 36, label='K')

        self.G.add_edge(16, 17, label='K')
        self.G.add_edge(16, 22, label='K')
        self.G.add_edge(16, 25, label='K')
        self.G.add_edge(16, 26, label='K')
        self.G.add_edge(16, 27, label='K')
        self.G.add_edge(16, 28, label='K')
        self.G.add_edge(16, 29, label='K')
        self.G.add_edge(16, 34, label='K')
        self.G.add_edge(16, 35, label='K')
        self.G.add_edge(16, 36, label='K')

        self.G.add_edge(17, 22, label='K')
        self.G.add_edge(17, 25, label='K')
        self.G.add_edge(17, 26, label='K')
        self.G.add_edge(17, 27, label='K')
        self.G.add_edge(17, 28, label='K')
        self.G.add_edge(17, 29, label='K')
        self.G.add_edge(17, 34, label='K')
        self.G.add_edge(17, 35, label='K')
        self.G.add_edge(17, 36, label='K')

        self.G.add_edge(22, 25, label='K')
        self.G.add_edge(22, 26, label='K')
        self.G.add_edge(22, 27, label='K')
        self.G.add_edge(22, 28, label='K')
        self.G.add_edge(22, 29, label='K')
        self.G.add_edge(22, 34, label='K')
        self.G.add_edge(22, 35, label='K')
        self.G.add_edge(22, 36, label='K')

        self.G.add_edge(25, 26, label='K')
        self.G.add_edge(25, 27, label='K')
        self.G.add_edge(25, 28, label='K')
        self.G.add_edge(25, 29, label='K')
        self.G.add_edge(25, 34, label='K')
        self.G.add_edge(25, 35, label='K')
        self.G.add_edge(25, 36, label='K')

        self.G.add_edge(26, 27, label='K')
        self.G.add_edge(26, 28, label='K')
        self.G.add_edge(26, 29, label='K')
        self.G.add_edge(26, 34, label='K')
        self.G.add_edge(26, 35, label='K')
        self.G.add_edge(26, 36, label='K')

        self.G.add_edge(27, 28, label='K')
        self.G.add_edge(27, 29, label='K')
        self.G.add_edge(27, 34, label='K')
        self.G.add_edge(27, 35, label='K')
        self.G.add_edge(27, 36, label='K')

        self.G.add_edge(28, 29, label='K')
        self.G.add_edge(28, 34, label='K')
        self.G.add_edge(28, 35, label='K')
        self.G.add_edge(28, 36, label='K')

        self.G.add_edge(29, 34, label='K')
        self.G.add_edge(29, 35, label='K')
        self.G.add_edge(29, 36, label='K')

        self.G.add_edge(34, 35, label='K')
        self.G.add_edge(34, 36, label='K')

        self.G.add_edge(35, 36, label='K')

    def asMultiGraph(self):
        return self.G

    def asOneGraph(self):
        return nx.Graph(self.G)

    def asDictOfGraphs(self):
        Graphs = {}
        for l in self.EdgeNames:
            FG = nx.Graph()
            FG.add_nodes_from(self.G)
            selected_edges = [(u, v, e) for u, v, e in self.G.edges(
                data=True) if e['label'] == l]
            FG.add_edges_from(selected_edges)
            Graphs[l] = FG
        return Graphs

    def printMulti(self):
        dot_G = nx.nx_pydot.to_pydot(self.G)
        print(dot_G)

    def drawMulti(self, filename='raj.png'):
        A = nx.nx_agraph.to_agraph(self.G)
        A.layout('dot')
        A.draw(filename)
