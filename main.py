import pickle as pkl
from os import path
import pandas as pd
from itertools import product
import hiplot as hip
import constants as cst
###############################################################################
# Read Data
###############################################################################
(PT_CLS, PT_DTA) = (cst.PT_CLS, cst.PT_DTA)
(dfChr, dfKrt) = [
    pd.read_csv(path.join(PT_DTA, fn)).set_index('Character')
    for fn in ('CharacterStats.csv', 'KartStats.csv')
]
clsList = pkl.load(open(path.join(PT_CLS, 'lst_clusters.pkl'), 'rb'))
clsListID = pkl.load(open(path.join(PT_CLS, 'lst_clustersID.pkl'), 'rb'))
dfCls = pd.DataFrame(clsListID, columns=['index', 'group'])
dfCls = dfCls.set_index('index')
###############################################################################
# All Combos
###############################################################################
(CHARS, KARTS) = (list(dfChr.index), list(dfKrt.index))
COMBOS = list(product(CHARS, KARTS))
dfCmb = pd.DataFrame({
    f'{c} - {k}':  dfChr.loc[c]+dfKrt.loc[k]
    for (c, k) in COMBOS
}).T
dfCmb = dfCmb.join(dfCls)
ixplit = [i.split('-') for i in dfCmb.index]
dfCmb['Racer'] = [
    i[0].strip().replace(' ', '') 
    for i in ixplit
]
dfCmb['Kart'] = [
    i[1].strip().replace(' ', '') 
    if len(i)==2 else
    '-'.join(i[1:]).replace(' ', '')
    for i in ixplit
]
dfCmb.rename({
    'SpSolid': 'SS', 'SpCoarse': 'SC', 'SpLiquid': 'SL', 
    'Accel': 'Acc', 'MiniT': 'MT', 'WeightCoin': 'W',
    'HdSolid': 'HS', 'HdCoarse': 'HC', 'HdLiquid': 'HL', 
    'Racer': 'Racer', 'Kart': 'Kart',
    'group': 'Grp'
}, axis=1, inplace=True)
cSort = [
    'Racer', 'Kart',
    'SS', 'SC', 'SL', 
    'HS', 'HC', 'HL',
    'Acc', 'MT', 'W'
][::-1]
###############################################################################
# HiPlot
###############################################################################
exp = hip.Experiment.from_dataframe(dfCmb.reset_index())
exp._display_data
exp.colormap = "interpolateSinebow"
exp.display_data(hip.Displays.PARALLEL_PLOT).update({
    'hide': ['uid', 'from_uid', 'Grp', 'Kart', 'Racer'],
    'order': cSort
})
exp.display_data(hip.Displays.TABLE).update({
    'hide': ['index', 'uid', 'from_uid'],
    'order': cSort[::-1]
})
exp.display(force_full_width=True)
_ = exp.to_html(path.join(cst.PT_PLT, 'parallel.html'))

