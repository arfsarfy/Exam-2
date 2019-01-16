import pandas as pd 
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
# import pandas as pd
from plotly import tools
from dash.dependencies import Input, Output


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

titanic = pd.read_csv('Titanic.csv')
titani_out= pd.read_csv('TitanicOutCalc.csv')



app = dash.Dash(__name__)  # external_stylesheets=external_stylesheets
server = app.server

dataset={"titanic":titanic,"titani_out":titani_out}

def getPlot(df_pokemon,jenis,x_axis,y_axis):
    list_gofunc={
    'bar':go.Bar,
    'violin':go.Violin,
    'box':go.Box
            }
    return [list_gofunc[jenis](
                x=df_pokemon[x_axis],
                y=df_pokemon['fare'],
                opacity=0.7,
                name='fare',
                marker=dict(color='#a5490b')
            )]



def call3(df_pokemon,jenis_plot,x_axis,go):
    return {'data':getPlot(df_pokemon,jenis_plot,x_axis),
        'layout':go.Layout(
        xaxis=dict(title=x_axis), yaxis=dict(title='fare'),
        margin=dict(l=40,b=40,t=10,r=10),
        # legend={'x':0,'y':1},
        hovermode='closest',
        boxmode='group',violinmode='group'
            )
        }





app.title = 'Dashboard Titanic'
app.layout = html.Div(children= [ 
                html.H1(children = 'Dashboard Titanic',className='titleDashboard'),
                dcc.Tabs(id="tabs", value='tab-4', children=[                                                                 #TABS HEAD
                    dcc.Tab(label='Titanic Dataset', value='tab-1', children=[                                                #TAB 1
                        html.Div([                                                              
                            html.H1('Table Data Titanic',className='h1_x'),
                            html.Br(),
                            html.Div(className='row justify-content-md-center', children=[
                                html.Div(className='col-sm-4',children=[
                                        html.P('dataset :',className='text_modified'),
                                        dcc.Dropdown(
                                                id='dataset',
                                                options=[{'label': i, 'value': i} for i in list(dataset.keys())],
                                                value='titanic',
                                                # style={'width':'300px'}
                                                    )
                                            ]
                                        ),      
                                
                                    ]),
                            html.Br(),
                            html.Br(),                                                                                
                            dcc.Graph(id='table', style={'overflowY': 'scroll', 'height': 600}),
                    ])
                            ]),
                    dcc.Tab(label='Categorical Plot', value='tab-2', children=[                                                   #TAB 2
                        html.Div([                                                          
                                    html.H1('Category Plot Titanic',className='h1_x'),
                                    html.Div('Plot Type',className='text_modified'),
                                    html.Div(className='row justify-content-md-center', children=[
                                        html.Div(className='col-6',children=[
                                            dcc.Dropdown(
                                                    id='jenisPlot',
                                                    options=[{'label': i, 'value': i.lower()} for i in ['Bar','Box','Violin']],
                                                    value='bar',
                                                    # style={'width':'300px'}
                                                        )
                                                ],
                                        # style={'margin':'0 auto'}
                                        )
                                        ]),
                                    html.Br(),
                                    html.Div(className='row justify-content-md-center', children=[
                                        html.Div('x-Axis   ',className='col-md-auto'),
                                        html.Div(className='col col-lg-2',children=[
                                            dcc.Dropdown(
                                                    id='x_axis',
                                                    options=[{'label': i, 'value': i} for i in titanic.columns],
                                                    value='survived',
                                                    # style={'width':'300px'}
                                                        )],
                                        # style={'margin':'0 auto'}
                                        ),
                                        

                                        ]),
                                    dcc.Graph(id='CategoricalPlot')                                                                                                              
                    ])
                        ]),
                            
            ],
            style={
                'fontFamily':'Arial'
                },
            content_style={
                'fontFamily':'Arial',
                'borderBottom' : '5px solid #d6d6d6',
                'borderLeft' : '5px solid #d6d6d6',
                'borderRight' : '5px solid #d6d6d6',
                'padding': '44px'
                })


                        
            ], 
            style={
                'maxWidth':'1200px',
                'margin':'0 auto' 
                    }
            )


@app.callback(
    Output(component_id='CategoricalPlot', component_property='figure'),
    [Input(component_id='jenisPlot', component_property='value'),
    Input(component_id='x_axis', component_property='value')])

def update_graphCategorical(jenis_plot,x_axis):
    return call3(titanic,jenis_plot,x_axis,go)


@app.callback(
    Output(component_id='table', component_property='figure'),
    [Input(component_id='dataset', component_property='value')])

def update_PieChart(ds):
    return go.Table(
                        header=dict(values=list(dataset[ds].columns),
                                    fill = dict(color='#C2D4FF'),
                                    align = ['left'] * 5),
                        cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
                                fill = dict(color='#F5F8FF'),
                                align = ['left'] * 5))





if __name__ == '__main__':
    #run server on port 1997
    #debug=True for auto restart if code edited
    app.run_server(debug=True)