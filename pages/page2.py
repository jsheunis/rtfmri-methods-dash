# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app

# Get data
filename = 'assets/rtfMRI_methods_review_included_studies_procsteps_DEFAULTS.txt'
df_studies = pd.read_csv(filename, sep='\t', lineterminator='\r')
df_studies = df_studies.dropna(axis='columns')
df_plot = df_studies.copy()

colnames = {
    'author':'Author',
    'vendor': 'Vendor',
    'magnet': 'Field strength',
    'software': 'Software',
    'stc': 'Slice time correction',
    'mc': '3D volume realignment',
    'ss': 'Spatial smoothing',
    'dr': 'Drift removal',
    'hmp': 'Realignment parameter regression',
    'ts': 'Temporal smoothing',
    'ff': 'Frequency filtering',
    'or': 'Outlier removal',
    'droi': 'Differential ROI',
    'resp': 'Respiratory noise removal',
    'doi': 'Article DOI'
}

plotnames = [
    {'label': 'Vendor', 'value': 'vendor'},
    {'label': 'Field strength', 'value': 'magnet'},
    {'label': 'Software', 'value': 'software'},
    {'label': 'Slice time correction', 'value': 'stc'},
    {'label': '3D volume realignment', 'value': 'mc'},
    {'label': 'Spatial smoothing', 'value': 'ss'},
    {'label': 'Drift removal', 'value': 'dr'},
    {'label': 'Realignment parameter regression', 'value': 'hmp'},
    {'label': 'Temporal smoothing', 'value': 'ts'},
    {'label': 'Frequency filtering', 'value': 'ff'},
    {'label': 'Outlier removal', 'value': 'or'},
    {'label': 'Differential ROI', 'value': 'droi'},
    {'label': 'Respiratory noise removal', 'value': 'resp'},
]

srs = df_plot['vendor'].value_counts()
xx = srs.index.to_list()
yy = srs.values

dataframe = df_plot.loc[df_plot['vendor'] == 'Siemens']
srs2 = dataframe['magnet'].value_counts()
xx2 = srs2.index.to_list()
yy2 = srs2.values


main_md = dcc.Markdown('''

In this section you can visualize and interact with the coded data from 128 real-tme fMRI neurofeedback studies.
There are two plots below, for which you can display data of a method selected from the respective dropdowns.

Say you want to view the distribution of scanner vendors used in these studies, select the `Vendor` option for the plot on the left hand side.
You can then *hover* over each of the bars in the plot to see the actual number of studies per vendor, e.g. 18 studies used a Philips scanner.
You can also *click* on the bar to display these specific studies in a table below the plots.

Say, now, that you want to see which software packages were used for each of the vendors, select the `Software` option for the plot on the right hand side.
By hovering over each bar on the `Vendor` plot, the `Software` plot will update with the relevant distribution.       

''')

layout = html.Div([
            html.Div([
                html.H2('Visualize'),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),
            html.Div(main_md,
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Br([]),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Dropdown(
                                id='drop-1',
                                options=plotnames,
                                value='vendor',
                                ),
                                width={"size": 4, "offset": 1}, # figure out offset
                            ),
                            dbc.Col(dcc.Dropdown(
                                id='drop-2',
                                options=plotnames,
                                value='vendor',
                                ),
                                width={"size": 4, "offset": 2},
                            ),
                        ],
                        justify="start"
                    ),
                    html.Br([]),
                    dbc.Row(
                        [
                            dbc.Col(html.H6(
                                id='graph-1-title',
                                children='Vendor (hover to show options of second feature; click to display studies)',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            ),
                            dbc.Col(html.H6(
                                id='graph-2-title',
                                children='Field strength options when Vendor = Siemens',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                dcc.Graph(
                                    id='graph-1',
                                    figure={
                                        'data': [
                                            {'x': xx, 'y': yy, 'type': 'bar', 'name': 'Vendors', 'marker': {'color': '#9EBC9F'}},
                                        ],
                                    }
                                ),
                            )),
                            dbc.Col(html.Div(
                               dcc.Graph(
                                id='graph-2',
                                    figure={
                                        'data': [
                                            {'x': xx2, 'y': yy2, 'type': 'bar', 'name': 'Field strength', 'marker': {'color': '#D3B88C'}},
                                        ],
                                    }
                                ),
                            )),
                        ]
                    ),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Div(
                id='table-1',
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            )
])


# Callback for updating graph 1
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-1-title', 'children')],
    [Input('drop-1','value')]
)
def update_graph(feature):

    srs = df_plot[feature].value_counts()
    xx = srs.index.to_list()
    yy = srs.values
    txt = colnames[feature]

    fig={
        'data': [
            {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#9EBC9F'}},
        ],
    }

    title = txt + ' (hover to show options of second feature; click to display studies)'

    return [fig, title]

# Callback for updating dropdown2 based on dropdown1 value
@app.callback(
    [Output('drop-2', 'options'),
     Output('drop-2', 'value')],
    [Input('drop-1','value')]
)
def reset_dropdown2_opts(value):
    plotnames_2 = [x for x in plotnames if x['value'] != value]
    value_2 = plotnames_2[0]['value']
    return plotnames_2, value_2


# Callback for updating graph 2 based on graph1 hoverData and dropdowns
@app.callback(
    [Output('graph-2', 'figure'),
     Output('graph-2-title', 'children')],
    [Input('graph-1', 'hoverData'),
     Input('drop-1','value'),
     Input('drop-2','value')]
)
def update_graph(hoverData, feature1, feature2):
    if hoverData is None or feature1 is None or feature2 is None:
        raise PreventUpdate
    else:
        x = hoverData['points'][0]['x']
        dataframe = df_plot.loc[df_plot[feature1] == x]
        srs = dataframe[feature2].value_counts()
        xx = srs.index.to_list()
        yy = srs.values
        txt = colnames[feature2] + ' options when ' + colnames[feature1] + ' = ' + x

        fig={
            'data': [
                {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#D3B88C'}},
            ],
        }

        title = txt

        return [fig, title]


# Callback for showing table 1 after filtering on feature 1
@app.callback(
    Output('table-1', 'children'),
    [Input('graph-1', 'clickData'),
     Input('drop-1','value')])
def generate_table(clickData, feature, max_rows=20):

    if clickData is None:
        raise PreventUpdate
    else:
        x = clickData['points'][0]['x']

        dataframe = df_plot.loc[df_plot[feature] == x]
        table=html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in list(colnames.values())])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(writeElement(i, col, dataframe)) for col in dataframe.columns],
                ) for i in range(min(len(dataframe), max_rows))
            ]),
            ],
            className='qcsummary',
        )

        # class="table-row" data-href="http://tutorialsplane.com"

        heading=html.H4('Showing studies where ' + colnames[feature] + ' = ' + x,
                        style={'textAlign': 'center',})

        # table = dbc.Table.from_dataframe(dataframe,
        #                                  striped=True,
        #                                  bordered=True,
        #                                  hover=True,
        #                                  responsive=True,
        #                                  className='qcsummary'
        #                                  )

        return [heading, table]


def writeElement(i, col, dataframe):
    if col == 'doi':
        hrf = 'https://doi.org/'+dataframe.iloc[i][col]
        return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    else:
        return dataframe.iloc[i][col]