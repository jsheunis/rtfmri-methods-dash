# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc

card_browse = [
    dbc.CardBody(
        [
            html.H5("Browse", className="card-title"),
            html.P(
                "This site contains a list of 128 recent studies in the field of real-time fMRI neurofeedback. Their methods were coded into a common structure, and this site allows you to explore these methods.",
                className="card-text",
            ),
            dbc.Button("Browse now", color="light", href="/pages/page1"),
        ]
    ),
]

card_visualize = [
    dbc.CardBody(
        [
            html.H5("Visualize", className="card-title"),
            html.P(
                "Want to see which methods are the most popular? Or how many studies reported implementing your favorite preprocessing step? Here you can view and interact with plots of the data.",
                className="card-text",
            ),
            dbc.Button("Visualize now", color="light", href="/pages/page2"),
        ]
    ),
]

card_submit = [
    dbc.CardBody(
        [
            html.H5("Submit", className="card-title"),
            html.P(
                "Have you conducted and reported a real-time fMRI study? Head to the submit page to report your methods. This functionality will allow you to create a machine readable methods section for you paper (tbc)",
                className="card-text",
            ),
            dbc.Button("Submit now", color="light", href="/pages/page3"),
        ]
    ),
]



layout = html.Div([

    html.H1(
        children='Real-time fMRI Neurofeedback Methods',
        style={
            'textAlign': 'center',
        }
    ),
    html.Br(),
    html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_browse, color="primary", inverse=True)),
                dbc.Col(
                    dbc.Card(card_visualize, color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_submit, color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        ]
    )

    # html.H2(children='Browse through literature to find and visualize studies and their methods',
    #          style={
    #     'textAlign': 'center',
    # }),



],
style={
    'marginBottom': 25,
    'marginTop': 50,
    'marginLeft': '5%',
    'maxWidth': '90%'
})
