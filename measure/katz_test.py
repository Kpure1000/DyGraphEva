from task_total import read_Graphs
from measurements import delta_sum, all_pairs_measure
from task2 import all_pairs_delta
import measurements as ms
import matplotlib.pyplot as plt


def wipe_repeated_pair_dict(nodes, all_paris):
    paris_d={}
    for s in range(0,len(nodes)):
        for t in range(0, len(nodes)):
            pair_st = (nodes[s],nodes[t])
            if (s != t) and ( pair_st not in paris_d and (nodes[t],nodes[s]) not in paris_d ):
                paris_d[pair_st]=all_paris[pair_st]
    return paris_d


# gs = read_Graphs("../data/dataset/synth/test0/", "test")
# gs = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
gs = read_Graphs("../data/dataset/synth/edge_eva/", "edge_eva")
# gs = read_Graphs("../data/dataset/synth/cluster/", "cluster")

# gs = read_Graphs("../data/dataset/truth/newcomb/", "newcomb")
# gs = read_Graphs("../data/dataset/truth/vdBunt_data/", "FR")


pl=[]
x=[]
for i in range(10):
    b = 0.01 * float(i + 1)
    x.append(b)
    nodes = list(gs[0].nodes)
    gs_measure = all_pairs_measure([ms.KatzIndex(g, b=b) for g in gs])
    all_paris_delta = ms.delta_sum(gs_measure)
    paris_d = wipe_repeated_pair_dict(nodes=nodes, all_paris=all_paris_delta)
    pl.append(paris_d)


pairs = list(pl[0])
legend=[]
for pair in pairs:
    y=[]
    for pd in pl:
        y.append(pd[pair])
    legend.append("pair[{0},{1}]".format(pair[0],pair[1]))
    plt.plot(x, y, '.-')

plt.legend(legend)
plt.show()
