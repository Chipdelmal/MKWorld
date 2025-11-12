import pickle as pkl
from os import path
from itertools import product
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback, dash_table
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
dfCls = pd.DataFrame(clsListID, columns=['index', 'Cluster'])
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
# Initial selection -----------------------------------------------------------
(cA, cB) = (
    'Yoshi - Standard Kart',
    'Toadette - Cute Scoot'
)
# Add 10 as offset to make all values positive --------------------------------
(pA, pB) = (
    dfCmb.loc[cA][cats]+10,
    dfCmb.loc[cB][cats]+10
)

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=pA, theta=cats, name=cA))
fig.add_trace(go.Scatterpolar(r=pB, theta=cats, name=cB))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=False, range=[0, 25])),
    width=1000,  height=1000, showlegend=True
)
fig.show()

###############################################################################
# Dash App
###############################################################################
charList = sorted(list(set(dfCmb['Racer'].values)))
kartList = sorted(list(set(dfCmb['Kart'].values)))

app = Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])
app.title = "MKWCombo"
app.layout = html.Div([
    dbc.Row([
        html.H1(
            'Mario Kart World: Combo Comparison',
            style={
                'textAlign': 'left',
                'paddingLeft': '2rem', 
                'paddingTop': '1rem', 'paddingBottom': '1rem',
                'color': '#F0F0F0', 'background-color': '#53629E'
            }
        )
    ]),
    dbc.Col([
        dbc.Row([
            # dbc.Col([], width=1),
            dbc.Col([
                html.H3('Combo A', style={
                    'color': '#4E56C0', 'paddingLeft': '2rem'
                }),
                dcc.Dropdown(
                    charList, 'Yoshi', id='charA',
                    style={'paddingLeft': '2rem'}
                ),
                dcc.Dropdown(
                    kartList, 'Standard Kart', id='kartA',
                    style={'paddingLeft': '2rem'}
                ),
            ], width=2),
            # dbc.Col([], width=1),
            dbc.Col([
                html.H3('Combo B', style={
                    'color': '#E45A92', 'paddingLeft': '2rem'
                }),
                dcc.Dropdown(
                    charList, 'Toadette', id='charB',
                    style={'paddingLeft': '2rem'}
                ),
                dcc.Dropdown(
                    kartList, 'Cute Scoot', id='kartB',
                    style={'paddingLeft': '2rem'}
                ),
            ], width=2)
        ]),
        html.Div(
            dbc.Row([
                # dbc.Col([], width=1),
                dbc.Col(dcc.Graph(figure=fig, id='radar')),
                dbc.Col([
                html.H3(
                    "Similar builds to Combo A", 
                    style={'color': '#4E56C0', 'paddingLeft': '0rem'}
                ),
                dash_table.DataTable(
                        id='tableCluster',
                        style_cell={'fontSize': 12, 'textAlign': 'center'},
                        style_header={'fontSize': 14, 'fontWeight': 'bold'},
                        style_cell_conditional=[
                            {'if': {'column_id': 'Racer'}, 'width': '100px'},
                            {'if': {'column_id': 'Kart'}, 'width': '100px'},
                            {'if': {'column_id': 'SS'}, 'width': '30px'},
                            {'if': {'column_id': 'SC'}, 'width': '30px'},
                            {'if': {'column_id': 'SL'}, 'width': '30px'},
                            {'if': {'column_id': 'HS'}, 'width': '30px'},
                            {'if': {'column_id': 'HC'}, 'width': '30px'},
                            {'if': {'column_id': 'HL'}, 'width': '30px'},
                            {'if': {'column_id': 'Acc'}, 'width': '30px'},
                            {'if': {'column_id': 'MT'}, 'width': '30px'},
                            {'if': {'column_id': 'W'}, 'width': '30px'},
                        ]
                    )
                ], style={'paddingRight': '4rem'}),
            ]), 
            id='plot'
        ),
    ]),
    dbc.Row([
        html.P(['SS: Speed Solid, SC: Speed Coarse, SL: Speed Liquid, HS: Handling Solid, HC: Handling Coarse, HL: Handling Liquid, Acc: Acceleration, MT: MiniTurbo, W: Weight/Coin']),
        html.Footer([
            "Analysis by ",
            html.A("chipdelmal", href='http://chipdelmal.github.io'),
            ". Have a look at my ",
            html.A("blogpost", href='http://chipdelmal.github.io/dataViz/2025-11-10-MKW.html'),
            " for more information about the stats and clustering, as well as the ",
            html.A("code and data sources", href='http://chipdelmal.github.io/dataViz/2025-11-10-MKW.html#code-repo-and-data-sources'),
            "!"
        ], style={'color': '#F0F0F0', 'background-color': '#53629E', 'paddingTop': '1rem', 'paddingBottom': '1rem', 'fontsize': 14, 'textAlign': 'right'}
        )
    ], style={
        'paddingTop': '1rem',
        'paddingLeft': '1rem', 
        'position': 'relative',
        'left': 0, 'bottom': 0, 'width': '100%'
    }),
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
        name=cA,
        line=dict(
            color='#4E56C0',
            width=5
        )
    ))
    fig.add_trace(go.Scatterpolar(
        r=pB, theta=cats,
        name=cB,
        line=dict(
            color='#E45A92',
            width=5
        )
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False,  range=[0, 25])
        ),
        font=dict(size=17.5),
        width=900, height=900,
        showlegend=False
    )
    return fig

@callback(
    Output(component_id='tableCluster', component_property='data'),
    Input('charA', 'value'), Input('kartA', 'value'),
    Input('charB', 'value'), Input('kartB', 'value'),
)
def update_table(charA, kartA, charB, kartB):
    clsA = int(dfCmb[
        (dfCmb['Racer']==charA) &
        (dfCmb['Kart']==kartA)
    ]['Cluster'])
    dfTmp = dfCmb[dfCmb['Cluster']==clsA]
    dfTmp = dfTmp[[
        'Racer', 'Kart', 
        'SS', 'SC', 'SL', 
        'HS', 'HC', 'HL',
        'Acc', 'MT', 'W', 
        # 'Cluster'
    ]]
    # print(dfTmp)
    return dfTmp.to_dict(orient='records')

if __name__ == '__main__':
    app.run(debug=False, port=8051)