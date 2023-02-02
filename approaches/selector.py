from Frishman import Frishman
from Aging import Aging
from Incremental import Incremental
from app_total import read_Graphs, save_Graphs
def Selector(pathIn, pathOut, name):
    Gs, d = read_Graphs(pathIn, name)

    # Gs = Frishman(Gs, iterations=200)
    # Gs = Aging(Gs, iterations=200, scale=1)
    Gs = Incremental(Gs, scale=1)

    save_Graphs(pathOut, name, Gs, d)


# Selector('../data/dataset/truth/mammalia-pa/','../data/selected/truth/mammalia-pa/','mammalia-pa')
# Selector('../data/dataset/truth/vdBunt_data/','../data/selected/truth/vdBunt_data/','FR')

# Selector('../data/dataset/truth/dblp/','../data/selected/truth/dblp/','dblp')
# Selector('../data/dataset/truth/canVote/','../data/selected/truth/canVote/','canVote')
# Selector('../data/dataset/truth/wildbird/','../data/selected/truth/wildbird/','wildbird')
Selector('../data/dataset/truth/InVS15/','../data/selected/truth/InVS15/','InVS15')
Selector('../data/dataset/truth/InVS13/','../data/selected/truth/InVS13/','InVS13')
# Selector('../data/dataset/truth/tortoise/','../data/selected/truth/tortoise/','tortoise')
# Selector('../data/dataset/truth/primary/','../data/selected/truth/primary/','primary')
