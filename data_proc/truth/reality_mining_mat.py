import scipy.io as sio

mat = sio.loadmat("../../data/dataset/truth/reality_mining/realitymining.mat")

keys = mat.keys()

print(keys)

mat['network']

# TODO: follow https://github.com/ElsaScola/reality-mining/blob/master/Reality-Mining.ipynb
