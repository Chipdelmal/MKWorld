import pickle as pkl
from os import path
from itertools import product
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
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
    i[0].strip().replace('', '') 
    for i in ixplit
]
dfCmb['Kart'] = [
    i[1].strip().replace('', '') 
    if len(i)==2 else
    '-'.join(i[1:]).replace('', '')
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
# Radial
###############################################################################
cats = list(dfCmb.columns)[:-3]
cats = [ 
    'MT', 'Acc', 
    'SS', 'SC', 'SL', 
    'HS', 'HC', 'HL',   
    'W',  
]


(cA, cB) = (
    'Yoshi - Standard Kart',
    'Toadette - Cute Scoot'
)

pA = dfCmb.loc[cA][cats]+10
pB = dfCmb.loc[cB][cats]+10

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
    r=pA, theta=cats,
    # fill='toself',
    name=cA
))
fig.add_trace(go.Scatterpolar(
    r=pB, theta=cats,
    # fill='toself',
    name=cB
))
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=False,
            range=[0, 25]
    )),
    width=1000,
    height=1000,
    showlegend=True
)
fig.show()




charList = sorted(list(set(dfCmb['Racer'].values)))
kartList = sorted(list(set(dfCmb['Kart'].values)))

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(charList, 'Yoshi', id='charA'),
            dcc.Dropdown(kartList, 'Standard Kart', id='kartA'),
        ], width=2),
        dbc.Col([
            dcc.Dropdown(charList, 'Toadette', id='charB'),
            dcc.Dropdown(kartList, 'Cute Scoot', id='kartB'),
        ], width=2),
    ]),
    html.Div(
        dcc.Graph(figure=fig, id='radar'), 
        id='plot'
    )
])
@callback(
    Output('radar', 'figure'),
    Input('charA', 'value'), Input('kartA', 'value'),
    Input('charB', 'value'), Input('kartB', 'value'),
)
def update_figure(charA, kartA, charB, kartB):

    (cA, cB) = (
        f'{charA} - {kartA}',
        f'{charB} - {kartB}'
    )

    pA = dfCmb.loc[cA][cats]+10
    pB = dfCmb.loc[cB][cats]+10


    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=pA, theta=cats,
        # fill='toself',
        name=cA
    ))
    fig.add_trace(go.Scatterpolar(
        r=pB, theta=cats,
        # fill='toself',
        name=cB
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False,
                range=[0, 25]
        )),
        width=1000,
        height=1000,
        showlegend=True
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8051)