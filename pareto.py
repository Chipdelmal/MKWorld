from os import path
import constants as cst
import pandas as pd
from paretoset import paretoset
from sklearn.manifold import TSNE
from umap import UMAP
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv(
    path.join(cst.PT_DTA, 'CombosClustered.csv')
)
dfTmp = df[[
    'SpSolid', 'SpCoarse', 'SpLiquid', 
    'Accel', 'MiniT', 
    # 'HdSolid', 'HdCoarse', 'HdLiquid'
]]

sense=['max']*dfTmp.shape[1]

mask = paretoset(dfTmp, sense=sense)
pareto = df[mask]
pareto.to_csv('./data/pareto.csv', index=False)


tsne = TSNE(n_components=2, random_state=0)
projections = tsne.fit_transform(pareto.iloc[:,1:])



umap_3d = UMAP(n_components=3, init='random', random_state=0)
projections = umap_3d.fit_transform(df.iloc[:,1:4])


ax = plt.figure().add_subplot(projection='3d')
ax.scatter(
    df['SpSolid']+10, 
    df['SpCoarse']+10, 
    df['SpLiquid']+10
)

fig_3d = px.scatter_3d(
    x=df['SpSolid']+10, 
    y=df['SpCoarse']+10, 
    z=df['SpLiquid']+10, 
    color=df['Cluster']
)
fig_3d.show()

fig = go.Figure(data=[go.Scatter3d(
    x=df['SpSolid']+10, 
    y=df['SpCoarse']+10, 
    z=df['SpLiquid']+10, 
    mode='markers',
    marker=dict(
        color=df['Cluster']
    ),
    text=df['Unnamed: 0'],
    hoverinfo='text+x+y+z'
)])
fig.show()