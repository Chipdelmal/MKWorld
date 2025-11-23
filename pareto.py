from os import path
import numpy as np
import constants as cst
import pandas as pd
from paretoset import paretoset
from sklearn.manifold import TSNE
from umap import UMAP
import umap.plot
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, HoverTool, CustomJSHover

df = pd.read_csv(
    path.join(cst.PT_DTA, 'CombosClustered.csv')
)
df.rename({'Unnamed: 0': 'Build'}, axis=1, inplace=True)
dfTmp = df[[
    'SpSolid', 'SpCoarse', 'SpLiquid', 
    'Accel', 'MiniT', 
    'HdSolid', 'HdCoarse', 'HdLiquid'
]]

# sense=['max']*dfTmp.shape[1]
# mask = paretoset(dfTmp, sense=sense)
# pareto = df[mask]
# pareto.to_csv('./data/pareto.csv', index=False)


# tsne = TSNE(n_components=2, random_state=0)
# projections = tsne.fit_transform(pareto.iloc[:,1:])



umapper = UMAP(
    densmap=True, # output_metric='haversine',
    n_components=2, metric='cosine',
    n_neighbors=80, min_dist=0.05,
    init='random', random_state=0
)
mapper = umapper.fit(df.iloc[:,1:])
projection = mapper.transform(df.iloc[:,1:])

df_hover = df[['Build']]
df_hover['Speed'] = [
    f'(S:{9+d[0]:02d}, C:{6+d[1]:02d}, L:{6+d[2]:02d})' 
    for (_, d) in (df[['SpSolid', 'SpCoarse', 'SpLiquid']]).iterrows()
]
df_hover['Handling'] = [
    f'(S:{d[0]:02d}, C:{d[1]:02d}, L:{d[2]:02d})' 
    for (_, d) in (df[['HdSolid', 'HdCoarse', 'HdLiquid']]).iterrows()
]
df_hover['Acc/MiniT'] = [
    f'(A:{7+d[0]:02d}, M:{7+d[1]:02d})'
    for (_, d) in df[['Accel', 'MiniT']].iterrows()
]
df_hover['Cluster'] = df[['Cluster']]
umap.plot.points(mapper, labels=df['Cluster'])
umap.plot.output_notebook()
p = umap.plot.interactive(
    mapper, point_size=5, 
    hover_data=df_hover, 
    labels=df['Cluster'], 
    width=1000, height=1000
)
# hover = HoverTool(tooltips=[
#     ("Build", "@Build"),
#     ("Speeds", "(@SpSolid, @SpCoarse, @SpLiquid)")
# ])
# p.add_tools(hover)
output_file("./plots/umap.html")
save(p)


umap.plot.show(p)
# umap.plot.connectivity(mapper)
umap.plot.diagnostic(mapper, diagnostic_type='pca')


ax = plt.figure().add_subplot(projection='3d')
ax.scatter(
    projection[:,0], 
    projection[:,1],
    projection[:,2],
)

fig = go.Figure(data=[go.Scatter3d(
    x=projection[:,0], 
    y=projection[:,1],
    z=projection[:,2], 
    mode='markers',
    marker=dict(
        color=df['Cluster']
    ),
    text=df['Unnamed: 0'],
    hoverinfo='text+x+y+z'
)])
fig.show()


# x = np.sin(mapper.embedding_[:, 0]) * np.cos(mapper.embedding_[:, 1])
# y = np.sin(mapper.embedding_[:, 0]) * np.sin(mapper.embedding_[:, 1])
# z = np.cos(mapper.embedding_[:, 0])
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.scatter(x, y, z, c=digits.target, cmap='Spectral')

# fig = go.Figure(data=[go.Scatter3d(
#     x=x, 
#     y=y,
#     z=z, 
#     mode='markers',
#     marker=dict(
#         color=df['Cluster']
#     ),
#     text=df['Unnamed: 0'],
#     hoverinfo='text+x+y+z'
# )])
# fig.show()

# ax = plt.figure().add_subplot(projection='3d')
# ax.scatter(
#     df['SpSolid']+10, 
#     df['SpCoarse']+10, 
#     df['SpLiquid']+10
# )

# fig_3d = px.scatter_3d(
#     x=df['SpSolid']+10, 
#     y=df['SpCoarse']+10, 
#     z=df['SpLiquid']+10, 
#     color=df['Cluster']
# )
# fig_3d.show()

fig = go.Figure(data=[go.Scatter3d(
    x=projection[:,0], 
    y=projection[:,1],
    z=projection[:,2], 
    mode='markers',
    marker=dict(
        color=df['Cluster']
    ),
    text=df['Unnamed: 0'],
    hoverinfo='text+x+y+z'
)])
fig.show()