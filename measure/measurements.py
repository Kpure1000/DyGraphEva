import networkx as nx
import numpy as np


class IMeasure:

    def __init__(self, G) -> None:
        self.G = G

    def get(self, s, t):
        pass


class ShortestPath(IMeasure):

    def __init__(self, G, weight='weight') -> None:
        super().__init__(G)
        self.weight = weight
        self.nodes = list(G.nodes)


    def get(self, s, t):
        try:
            return 1.0 / nx.shortest_path_length(G=self.G,
                                               source=self.nodes[s],
                                               target=self.nodes[t],
                                               weight=self.weight)
        except: # networkx.exception.NetworkXNoPath
            return 0.0


class KatzIndex(IMeasure):

    def __init__(self, G, weight='weight', b=0.099999) -> None:
        '''
        b : float, control the beta, 
            which is a free parameter used to control path weights
        '''
        super().__init__(G)
        A = nx.adjacency_matrix(G=G,weight=weight).toarray()
        I = np.identity(len(G))
        eigen_max = np.amax(np.double(nx.adjacency_spectrum(G)))
        Beta = b * (1.0 / eigen_max)  # Beta is a free parameter
        self.S = np.linalg.inv(I - Beta * A) - I


    def get(self, s, t):
        return self.S[s][t]


class MCT(IMeasure):

    def __init__(self, G, weight='weight') -> None:
        super().__init__(G)
        L = nx.laplacian_matrix(G=G,weight=weight).toarray()
        self.CTK = np.linalg.pinv(L)


    def get(self, s, t):
        return self.CTK[s][s] + self.CTK[t][t] - 2 * self.CTK[s][t]


class ACT(IMeasure):

    def __init__(self, G, weight='weight') -> None:
        super().__init__(G)
        L = nx.laplacian_matrix(G=G,weight=weight).toarray()
        self.CTK = np.linalg.pinv(L)


    def get(self, s, t):
        val = (self.CTK[s][s] + self.CTK[t][t] - 2 * self.CTK[s][t])
        if val != 0:
            return 1/(self.CTK[s][s] + self.CTK[t][t] - 2 * self.CTK[s][t])
        else:
            return 0


def all_pairs_measure(measure_list):
    gs_measure=[]
    for measure in measure_list:
        nodes = list(measure.G.nodes)
        g_measure = {}
        for s in range(len(nodes)):
            for t in range(len(nodes)):
                if s != t:
                    g_measure[(nodes[s], nodes[t])] = measure.get(s, t)
        gs_measure.append(g_measure)

    return gs_measure


def delta_sum(gs_metrics):
    keys_delta={}
    for key in gs_metrics[0]:
        delta_val=0
        for i in range(0, len(gs_metrics)-1):
            if i+1!=len(gs_metrics):
                delta_val += abs( gs_metrics[i+1][key] - gs_metrics[i][key] )
        keys_delta[key] = delta_val
    return keys_delta
