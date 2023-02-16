import networkx as nx
import numpy as np

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)


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
        self.G = G
        self.ps = nx.shortest_path(G=G, weight=weight)


    def get(self, s, t):
        sp = 0
        nodes = self.ps[self.nodes[s]][self.nodes[t]]
        for i, n in enumerate(nodes):
            if i < len(nodes) - 1:
                sp += self.G[nodes[i]][nodes[i + 1]][self.weight]

        return sp
        # try:
        #     # return 1.0 / nx.shortest_path_length(G=self.G,
        #     #                                    source=self.nodes[s],
        #     #                                    target=self.nodes[t],
        #     #                                    weight=self.weight)
        #     # return nx.shortest_path_length(G=self.G,
        #     #                                    source=self.nodes[s],
        #     #                                    target=self.nodes[t],
        #     #                                    weight=self.weight)
        # except: # networkx.exception.NetworkXNoPath
        #     return 0.0


class KatzIndex(IMeasure):

    def __init__(self, G, weight='weight', b=0.099999) -> None:
        '''
        b : float, control the beta, 
            which is a free parameter used to control path weights
        '''
        super().__init__(G)
        A = nx.adjacency_matrix(G=G,weight=weight).toarray()
        I = np.identity(len(G))
        # eigen_max = np.amax(np.double(nx.adjacency_spectrum(G))) # ! nx spectrum is comlex number !
        eigen_max = np.amax(np.double(np.linalg.eigvals(A)))
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
        # val = val if val >= 1e-5 else 1e-5
        return 1.0 / (val + 1e-5)
        # if val != 0:
        #     return 1.0/val
        # else:
        #     return 0


class RWR(IMeasure):

    def __init__(self, G, weight='weight', alpha=0.6) -> None:
        super().__init__(G)

        import scipy as sp

        # A = nx.to_scipy_sparse_array(G, weight=weight, format="csr")
        A = nx.adjacency_matrix(G, weight=weight, dtype=float).toarray()
        # TODO: rm csr_array wrapper when spdiags can produce arrays
        Dvec = np.sum(A, axis=0,)
        Drec=[]
        for d in Dvec:
            if d == 0.0: Drec.append(0.0)
            else: Drec.append(1.0 / d)
        P = np.multiply(np.array(Drec), A)
        Pt = np.transpose(P)
        I = np.identity(len(G))
        self.q = alpha * np.linalg.inv(I - (1 - alpha) * Pt)


    def get(self, s, t):
        return self.q[s][t] + self.q[t][s]


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
