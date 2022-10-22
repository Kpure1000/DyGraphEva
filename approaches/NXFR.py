from copy import deepcopy
from json import dumps
import pickle
from app_total import read_Graphs
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from FR import fr_iterator

# gs, distance_scale = read_Graphs("../data/dataset/synth/test0/", "test")
# gs, distance_scale = read_Graphs("../data/dataset/synth/node_eva/", "node_eva")
gs, distance_scale = read_Graphs("../data/dataset/synth/node_add/", "node_add")
# gs, distance_scale = read_Graphs("../data/dataset/synth/cube/", "cube")


glen = len(gs)
fig, ax = plt.subplots(nrows=1, ncols=glen)
# fig = plt.figure()
# plt.xlim(-2., 2.)
# plt.ylim(-2., 2.)
# fig.set_size_inches(5, 5)
# plt.get_current_fig_manager().set_window_title("FR force-directed test")
fig.suptitle("`Fruchterman-Reingold`")


def OnlineDraw(ax, Gi, Li_1=None):
    if Li_1!=None:
        # Li = nx.fruchterman_reingold_layout(G=Gi, pos=Li_1)
        Li = fr_iterator(G=Gi, init_pos=Li_1, distance_scale=distance_scale)
    else:
        # Li = nx.fruchterman_reingold_layout(Gi)
        Li = fr_iterator(G=Gi,distance_scale=distance_scale)

    nx.draw_networkx(
        G=Gi,
        pos=Li,
        node_size=80,
        node_shape="o",
        edge_color="#aaa",
        width=1.5,
        font_size=6,
        font_color="#fff",
        ax=ax
    )

    return Li


Li_1=None
axr=list(ax)
axc=list(axr)
for i in range(0, glen):
    # axc[i].set_xlim(-2.0,2.0)
    # axc[i].set_ylim(-2.0,2.0)
    if i==0:
        Li_1 = OnlineDraw(ax=axc[i], Gi=gs[i])
    else:
        Li_1 = OnlineDraw(ax=axc[i], Gi=gs[i], Li_1=Li_1)


plt.show()