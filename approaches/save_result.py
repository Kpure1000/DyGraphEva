from app_total import save_Graphs, read_Graphs
from Aging import Aging
from Frishman import Frishman


def Get_Result(pathIn, nameIn, pathOut, nameOut):
    gs, distance_scale = read_Graphs(pathIn, nameIn)

    gs_out = Frishman(gs=gs, distance_scale=distance_scale)
    # gs_out = Aging(gs=gs, distance_scale=distance_scale, beta=2)

    save_Graphs(pathOut, nameOut, gs_out, distance_scale)
    print("save suc")


Get_Result("../data/dataset/synth/test0/", "test", "../data/result/synth/test/", "test_Frishman")
Get_Result("../data/dataset/synth/node_eva/", "node_eva", "../data/result/synth/node_eva/", "node_eva_Frishman")
Get_Result("../data/dataset/synth/node_add/", "node_add", "../data/result/synth/node_add/", "node_add_Frishman")
Get_Result("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Frishman")
Get_Result("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Frishman")
Get_Result("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Frishman")


# Get_Result("../data/dataset/synth/test0/", "test", "../data/result/synth/test/", "test_Aging")
# Get_Result("../data/dataset/synth/node_eva/", "node_eva", "../data/result/synth/node_eva/", "node_eva_Aging")
# Get_Result("../data/dataset/synth/node_add/", "node_add", "../data/result/synth/node_add/", "node_add_Aging")
# Get_Result("../data/dataset/truth/newcomb/", "newcomb", "../data/result/truth/newcomb/", "newcomb_Aging")
# Get_Result("../data/dataset/truth/vdBunt_data/", "FR", "../data/result/truth/vdBunt_data/", "FR_Aging")
# Get_Result("../data/dataset/truth/vdBunt_data/", "VRND32T", "../data/result/truth/vdBunt_data/", "VRND32T_Aging")
