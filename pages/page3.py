# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
import urllib.parse
import json

# Get data
filename = 'assets/rtfMRI_methods_review_included_studies_procsteps.txt'
df_studies = pd.read_csv(filename, sep='\t', lineterminator='\r')
df_studies = df_studies.dropna(axis='columns')

colnames = {
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

options_df = df_studies.copy()
df = options_df.drop(columns='author')
df = df.drop(columns='doi')

input_options = {}
for key in colnames.keys():
    srs = df[key].value_counts()
    xx = srs.index.to_list()
    yy = srs.values
    input_options[key] = [{'label': val, 'value': val} for val in xx]


heading = html.Div(
    html.H3('Visualize'),
    style={
        'marginBottom': 25,
        'marginTop': 25,
        'marginLeft': '5%',
        'maxWidth': '90%',
        'textAlign': 'center'
    }
)

main_md = dcc.Markdown('''

The purpose of this section is to allow you to report the methods of your real-time fMRI neurofeedback study in detail.
The use of validated text fields, dropdowns and checkboxes makes this process quick and intuitive, while improving standardisation.

This section still needs some work. Currently, the entry fields (and their options) below are populated from the [main study data](https://github.com/jsheunis/quality-and-denoising-in-rtfmri-nf).
This will be updated in future so as to allow a wider variety of input options. 

When you click on the `Submit` button, it will download an admittedly badly formatted `csv`-file containing your input data.
The goal is to improve this machine-readable output substantially and to automatically add it to this database of studies.
Additionally, it will also generate human-readable sentences (containing your entered data) that you can use when writing the methods section of an article.    

''')


section1 = dbc.Row(
    [

        dbc.Col([
            dbc.FormGroup(
                [
                    dbc.Label("Author and Date", html_for="author"),
                    dbc.Input(
                        type="text",
                        id="author",
                        placeholder="e.g. Heunis et al. (2018)",
                        bs_size="sm",
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Article DOI", html_for="doi"),
                    dbc.Input(
                        type="text",
                        id="doi",
                        placeholder="e.g. 10.31219/osf.io/xubhq",
                        bs_size="sm",
                    ),
                ]
            )],
            width=5,
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label("Article Title", html_for="article-title"),
                    dbc.Textarea(
                        id="article-title",
                        placeholder="e.g. Quality and denoising in real-time fMRI neurofeedback: a methods review",
                    ),
                ]
            ),
            width={"size": 5, "offset": 1},
        ),
    ],
    justify="start",
    form=True,
)


section2 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label(colnames[value], html_for=value),
                    dcc.Dropdown(
                        id=value,
                        options=input_options[value],
                    )
                ]
            ),
            width={"size": 3}, # figure out offset
        ) for value in ['vendor', 'magnet', 'software']

    ],
    justify="start",
    form=True,
)

section3 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label(colnames[value], html_for=value),
                    dcc.Dropdown(
                        id=value,
                        options=input_options[value],
                    )
                ]
            ),
            width={"size": 3}, # figure out offset
        ) for value in ['stc', 'mc', 'ss', 'dr']

    ],
    justify="start",
    form=True,
)

section4 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label(colnames[value], html_for=value),
                    dcc.Dropdown(
                        id=value,
                        options=input_options[value],
                    )
                ]
            ),
            width={"size": 3}, # figure out offset
        ) for value in ['hmp', 'ts', 'ff', 'or']

    ],
    justify="start",
    form=True,
)

section5 = dbc.Row(
    [
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label(colnames['droi'], html_for='droi'),
                    dcc.Dropdown(
                        id='droi',
                        options=input_options['droi'],
                    )
                ]
            ),
            width={"size": 3}, # figure out offset
        ),
        dbc.Col(
            dbc.FormGroup(
                [
                    dbc.Label(colnames['resp'], html_for='resp'),
                    dbc.Checklist(
                        id='resp',
                        options=input_options['resp'],
                        value=[],
                    ),

                ]
            ),
            width={"size": 3}, # figure out offset
        ),

    ],
    justify="start",
    form=True,
)


layout = html.Div([
    html.H2('Submit',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    main_md,
    html.Br([]),
    html.H4(['Study details']),
    html.Br([]),
    section1,
    html.Br([]),
    html.H4(['Hardware and software']),
    html.Br([]),
    section2,
    html.Br([]),
    html.H4(['Processing steps']),
    html.Br([]),
    section3,
    section4,
    section5,
    html.Br([]),
    dbc.Button("Submit", id='submit', color="primary", href=""),
    html.Br([]),
    html.Div(id='show-submit')
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})


@app.callback(Output('submit', 'href'),
              [Input('submit', 'n_clicks')],
              [State(value, 'value') for value in colnames.keys()])
def update_output(n_clicks, *selected_vals):

    data = {}
    for i, key in enumerate(colnames.keys()):
        data[key] = selected_vals[i]

    df = pd.DataFrame.from_dict(data)
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    # file_object = open('rtfmri_methods.txt', 'w')
    # json_data = json.dump(data, file_object)
    # json_data = json.dumps(data)
    # json_string = "data:text/html;charset=utf-8," + urllib.parse.quote(json_data)

    return csv_string
