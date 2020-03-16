# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app, server
from pages import home, page1, page2, page3



nav_item1 = dbc.NavItem(dbc.NavLink("Browse", href="/pages/page1"))
nav_item2 = dbc.NavItem(dbc.NavLink("Visualize", href="/pages/page2"))
nav_item3 = dbc.NavItem(dbc.NavLink("Submit", href="#"))
server


app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src='assets/logo_jsheunis_3.jpeg', height="30px", className="avatar")),
                            dbc.Col(dbc.NavbarBrand("rtfMRI Methods", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item1, nav_item2, nav_item3], className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="mb-5",
    ),

    html.Div(id='page-content')
    ]

)



###########################
# CALLBACKS AND FUNCTIONS #
###########################

# the same function (toggle_navbar_collapse) is used in all three callbacks
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open): # we use a callback to toggle the collapse on small screens
    if n:
        return not is_open
    return is_open


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/pages/page1':
        return page1.layout
    elif pathname == '/pages/page2':
        return page2.layout
    else:
        return '404'



##############
# RUN SERVER #
##############

if __name__ == '__main__':
    app.run_server(debug=True)