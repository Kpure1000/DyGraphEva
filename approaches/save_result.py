from app_total import save_Graphs, read_Graphs
from Aging import Aging
from Frishman import Frishman
from Incremental import Incremental
from Laplacian import Laplacian
import networkx as nx

def Get_Result_Frishman(pathIn, nameIn, pathOut, nameOut):
    gs, distance_scale = read_Graphs(pathIn, nameIn)

    gs_out = Frishman(gs=gs, k=0.1, iterations=250, weight='weight')

    save_Graphs(pathOut, nameOut, gs_out, 100.0)
    print("Frishman {0} save suc".format(nameIn))

def Get_Result_Aging(pathIn, nameIn, pathOut, nameOut):
    gs, distance_scale = read_Graphs(pathIn, nameIn)

    gs_out = Aging(gs=gs, beta=0.1, k=0.1, iterations=250, weight='weight')

    save_Graphs(pathOut, nameOut, gs_out, 100.0)
    print("Aging {0} save suc".format(nameIn))


def Get_Result_Incremental(pathIn, nameIn, pathOut, nameOut):
    gs, d = read_Graphs(pathIn, nameIn)

    gs_out = Incremental(gs=gs, weight='weight', C=4.0, dl=0.055, K=1.0)

    save_Graphs(pathOut, nameOut, gs_out, 100.0)
    print("Incremental {0} save suc".format(nameIn))


def Get_Result_Laplacian(pathIn, nameIn, pathOut, nameOut):
    gs, d = read_Graphs(pathIn, nameIn)

    gs_out = Laplacian(Gs=gs,
                       weight='weight',
                       seed=0,
                       alpha=1.0,
                       iterations=250)

    save_Graphs(pathOut, nameOut, gs_out, 100.0)
    print("Laplacian {0} save suc".format(nameIn))



# Get_Result_Frishman("../data/dataset/synth/cluster/", "cluster", "../data/result/synth/cluster/", "cluster_Frishman")
# Get_Result_Frishman("../data/dataset/synth/intra_cluster/", "intra_cluster", "../data/result/synth/intra_cluster/", "intra_cluster_Frishman")
# Get_Result_Frishman("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Frishman")
# Get_Result_Frishman("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Frishman")
# Get_Result_Frishman("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Frishman")
# Get_Result_Frishman("../data/dataset/truth/mammalia-pa/", "mammalia-pa", "../data/result/truth/mammalia-pa/", "mammalia-pa_Frishman")
# Get_Result_Frishman("../data/dataset/truth/dblp/", "dblp", "../data/result/truth/dblp/", "dblp_Frishman")
# Get_Result_Frishman("../data/dataset/truth/canVote/", "canVote", "../data/result/truth/canVote/", "canVote_Frishman")
# Get_Result_Frishman("../data/dataset/truth/wildbird/", "wildbird", "../data/result/truth/wildbird/", "wildbird_Frishman")
# Get_Result_Frishman("../data/dataset/truth/InVS15/", "InVS15", "../data/result/truth/InVS15/", "InVS15_Frishman")
# Get_Result_Frishman("../data/dataset/truth/InVS13/", "InVS13", "../data/result/truth/InVS13/", "InVS13_Frishman")
# Get_Result_Frishman("../data/dataset/truth/primary/", "primary", "../data/result/truth/primary/", "primary_Frishman")
# Get_Result_Frishman("../data/dataset/truth/reality_mining/", "reality_mining", "../data/result/truth/reality_mining/", "reality_mining_Frishman")
# Get_Result_Frishman("../data/dataset/truth/ambassador/", "ambassador", "../data/result/truth/ambassador/", "ambassador_Frishman")

# Get_Result_Aging("../data/dataset/synth/cluster/", "cluster", "../data/result/synth/cluster/", "cluster_Aging")
# Get_Result_Aging("../data/dataset/synth/intra_cluster/", "intra_cluster", "../data/result/synth/intra_cluster/", "intra_cluster_Aging")
# Get_Result_Aging("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Aging")
# Get_Result_Aging("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Aging")
# Get_Result_Aging("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Aging")
# Get_Result_Aging("../data/dataset/truth/mammalia-pa/", "mammalia-pa", "../data/result/truth/mammalia-pa/", "mammalia-pa_Aging")
# Get_Result_Aging("../data/dataset/truth/dblp/", "dblp", "../data/result/truth/dblp/", "dblp_Aging")
# Get_Result_Aging("../data/dataset/truth/canVote/", "canVote", "../data/result/truth/canVote/", "canVote_Aging")
# Get_Result_Aging("../data/dataset/truth/wildbird/", "wildbird", "../data/result/truth/wildbird/", "wildbird_Aging")
# Get_Result_Aging("../data/dataset/truth/InVS15/", "InVS15", "../data/result/truth/InVS15/", "InVS15_Aging")
# Get_Result_Aging("../data/dataset/truth/InVS13/", "InVS13", "../data/result/truth/InVS13/", "InVS13_Aging")
# Get_Result_Aging("../data/dataset/truth/primary/", "primary", "../data/result/truth/primary/", "primary_Aging")
# Get_Result_Aging("../data/dataset/truth/reality_mining/", "reality_mining", "../data/result/truth/reality_mining/", "reality_mining_Aging")
# Get_Result_Aging("../data/dataset/truth/ambassador/", "ambassador", "../data/result/truth/ambassador/", "ambassador_Aging")

# Get_Result_Incremental("../data/dataset/synth/cluster/", "cluster", "../data/result/synth/cluster/", "cluster_Incremental")
# Get_Result_Incremental("../data/dataset/synth/intra_cluster/", "intra_cluster", "../data/result/synth/intra_cluster/", "intra_cluster_Incremental")
# Get_Result_Incremental("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Incremental")
# Get_Result_Incremental("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Incremental")
# Get_Result_Incremental("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Incremental")
# Get_Result_Incremental("../data/dataset/truth/mammalia-pa/", "mammalia-pa", "../data/result/truth/mammalia-pa/", "mammalia-pa_Incremental")
# Get_Result_Incremental("../data/dataset/truth/dblp/", "dblp", "../data/result/truth/dblp/", "dblp_Incremental")
# Get_Result_Incremental("../data/dataset/truth/canVote/", "canVote", "../data/result/truth/canVote/", "canVote_Incremental")
# Get_Result_Incremental("../data/dataset/truth/wildbird/", "wildbird", "../data/result/truth/wildbird/", "wildbird_Incremental")
# Get_Result_Incremental("../data/dataset/truth/InVS15/", "InVS15", "../data/result/truth/InVS15/", "InVS15_Incremental")
# Get_Result_Incremental("../data/dataset/truth/InVS13/", "InVS13", "../data/result/truth/InVS13/", "InVS13_Incremental")
# Get_Result_Incremental("../data/dataset/truth/primary/", "primary", "../data/result/truth/primary/", "primary_Incremental")
# Get_Result_Incremental("../data/dataset/truth/reality_mining/", "reality_mining", "../data/result/truth/reality_mining/", "reality_mining_Incremental")
# Get_Result_Incremental("../data/dataset/truth/ambassador/", "ambassador", "../data/result/truth/ambassador/", "ambassador_Incremental")

# Get_Result_Laplacian("../data/dataset/synth/cluster/", "cluster", "../data/result/synth/cluster/", "cluster_Laplacian")
# Get_Result_Laplacian("../data/dataset/synth/intra_cluster/", "intra_cluster", "../data/result/synth/intra_cluster/", "intra_cluster_Laplacian")
# Get_Result_Laplacian("../data/dataset/synth/lap/", "lap", "../data/result/synth/lap/", "lap_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/mammalia-pa/", "mammalia-pa", "../data/result/truth/mammalia-pa/", "mammalia-pa_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/dblp/", "dblp", "../data/result/truth/dblp/", "dblp_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/canVote/", "canVote", "../data/result/truth/canVote/", "canVote_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/wildbird/", "wildbird", "../data/result/truth/wildbird/", "wildbird_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/InVS15/", "InVS15", "../data/result/truth/InVS15/", "InVS15_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/InVS13/", "InVS13", "../data/result/truth/InVS13/", "InVS13_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/primary/", "primary", "../data/result/truth/primary/", "primary_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/reality_mining/", "reality_mining", "../data/result/truth/reality_mining/", "reality_mining_Laplacian")
# Get_Result_Laplacian("../data/dataset/truth/ambassador/", "ambassador", "../data/result/truth/ambassador/", "ambassador_Laplacian")
