import numpy as np
from os import path
import pandas as pd
import pickle as pkl
from tqdm import tqdm
from itertools import product
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_distances, euclidean_distances, manhattan_distances
import constants as cst
###############################################################################
# Read Data
###############################################################################
(MDISTANCE, NCST) = (cst.MDISTANCE, cst.NUM_CLUSTER)
(PT_DTA, PT_CLS) = (cst.PT_DTA, cst.PT_CLS)
(dfChr, dfKrt) = [
    pd.read_csv(path.join(PT_DTA, fn)).set_index('Character')
    for fn in ('CharacterStats.csv', 'KartStats.csv')
]
###############################################################################
# All Combos
###############################################################################
(CHARS, KARTS) = (list(dfChr.index), list(dfKrt.index))
COMBOS = list(product(CHARS, KARTS))
dfCmb = pd.DataFrame({
    f'{c} - {k}':  dfChr.loc[c]+dfKrt.loc[k]
    for (c, k) in COMBOS
}).T
###############################################################################
# Read Data
###############################################################################
cFun = AgglomerativeClustering(n_clusters=NCST)
cluster_labels = cFun.fit_predict(dfCmb)
clList= list(zip(dfCmb.index, cluster_labels))
values = set(map(lambda x:x[1], clList))
clustersList = [[y[0] for y in clList if y[1]==x] for x in values]
pkl.dump(clustersList, open(path.join(PT_CLS, 'lst_clusters.pkl'), 'wb'))
pkl.dump(clList, open(path.join(PT_CLS, 'lst_clustersID.pkl'), 'wb'))
###############################################################################
# Calculate distance matrix
#   cosine_distances, euclidean_distances, manhattan_distances
###############################################################################
if MDISTANCE=='cosine':
    mfun = cosine_distances
elif MDISTANCE=='manhattan':
    mfun = manhattan_distances
else:
    mfun = euclidean_distances
pairs = list(dfCmb.index)[:]
pkl.dump(pairs, open(path.join(PT_CLS, 'lst_combos.pkl'), 'wb'))
# Generate matrix -------------------------------------------------------------
mat = []
for i in tqdm(pairs):
    cRow = mfun(np.array([dfCmb.loc[i]]), np.array(dfCmb))[0]
    mat.append(cRow)
mat = np.array(mat)
np.save(path.join(PT_CLS, f'mat_{MDISTANCE}.npy'), mat)