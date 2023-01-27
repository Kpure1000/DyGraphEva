from Frishman import Frishman
from Aging import Aging
from app_total import read_Graphs, save_Graphs
def Selector(pathIn, pathOut, name):
    Gs, d = read_Graphs(pathIn, name)

    # Gs = Frishman(Gs, iterations=200)
    Gs = Aging(Gs, iterations=200, scale=1)

    save_Graphs(pathOut, name, Gs, d)


# Selector('../data/dataset/truth/mammalia-pa/','../data/selected/truth/mammalia-pa/','mammalia-pa')
# Selector('../data/dataset/truth/vdBunt_data/','../data/selected/truth/vdBunt_data/','FR')

Selector('../data/dataset/truth/dblp/','../data/selected/truth/dblp/','dblp')
