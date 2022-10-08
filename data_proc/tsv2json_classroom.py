import pandas as pd

vert = pd.read_csv("../data/dataset/truth/classroom/classroom_vertices.tsv", sep='\t')

edge = pd.read_csv("../data/dataset/truth/classroom/classroom_edges.tsv", sep='\t')

a = edge['interaction_type'].unique()

print(a)


