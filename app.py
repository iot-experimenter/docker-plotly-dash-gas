import pandas as pd
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime as dt
#from datetime import timedelta, date
import numpy as np
import plotly.express as px
#import plotly.plotly as py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import dash_bootstrap_components as dbc
import json
import base64
#from python.data import Data
#from python.result import Result
import dash_daq as daq
import flask

def encode_image(image_file):
    encoded = base64.b64encode(open(image_file, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded.decode())


server = flask.Flask(__name__)

#def encode_jpgimage(image_jpgfile):
encodedjpg = base64.b64encode(open('assets/foto.jpg', 'rb').read())
#    return 'data:image/jpg;base64,{}'.format(encodedjpg.decode())


gaskaart = px.scatter_mapbox(
                        lat=38.92,
                        lon=-77.07,
                        size_max=20,
                        zoom=6

                        )

gaskaart.update_layout(mapbox_style="open-street-map",showlegend=False)
gaskaart.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



""" ************ layout ************ """
#external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']
external_stylesheets = [dbc.themes.CYBORG]

app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True



# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "black",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


theme =  {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
}

CARD_TEXT_STYLE_subtitel = {
    'textAlign': 'left',
    'color': 'yellow'
}

content = html.Div(id="page-content", style=CONTENT_STYLE)


sidebar = html.Div(
    [
        html.H6(dt.now().strftime('%Y-%m-%d'), className="display-6"),
        html.H6(dt.now().strftime('%H:%M:%S'), className="display-6"),

        html.Hr(),
        html.P(
            "Maak hier uw keuze", className="lead"
        ),

        dbc.Nav(
            [
                dbc.NavLink("Gas", href="/page-1", id="page-1-link"),
                dbc.NavLink("Pagina 2", href="/page-2", id="page-2-link"),
                dbc.NavLink("Pagina 3", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

GasKabineLabel = [

        dbc.CardHeader([html.H4("kabinenummer")]),
        dbc.CardBody([

            html.H6("Straat : ", className="text-body"),
            html.H5("Straat", className="text-white"),

            html.H6("Gebouw : ", className="text-body"),
            html.H5("Gebouw", className="text-white"),

            html.H6("Type:", className="text-body"),
            html.H5("Type", className="text-white"),

            html.H6("Gemeente:", className="text-body"),
            html.H5("Gemeente", className="text-white"),
        ]),
    ]

EVHILabel = [

        dbc.CardHeader([html.H4("EVHI")]),
        dbc.CardBody([

            dbc.Row([

                dbc.Col(xs=3,children=[
                      html.H6("gasflow : ", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                      html.H5("94,8 Nm³/h", className="text-meting"),
                ]), # einde col
                dbc.Col(xs=9,children=[

                        daq.GraduatedBar(
                                id='gasflow-bar',
                                size=400,
                                min=0, max=100,
                                step=2,
                                color={"ranges":{"green":[0,75],"yellow":[76,90],"red":[91,100]}},
                                style={'font-size': '14pt', 'font-family': 'Verdana','color':'black', 'font-weight': 'bold'},
                                showCurrentValue=True,
                                value=95
                                ),

                ]), # einde col

            ]), # einde rij

            dbc.Row([

                dbc.Col(xs=3,children=[
                       html.H6("druk:", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                       html.H5("4,2 bar", className="text-meting"),
                ]), # einde col
                dbc.Col(xs=9,children=[

                        daq.GraduatedBar(
                                id='druk-bar',
                                size=400,
                                min=0, max=100,
                                step=2,
                                color={"ranges":{"green":[0,75],"yellow":[76,90],"red":[91,100]}},
                                style={'font-size': '14pt', 'font-family': 'Verdana','color':'black', 'font-weight': 'bold'},
                                showCurrentValue=True,
                                value=77,
                                ),

                ]), # einde col

            ]), # einde rij

            dbc.Row([

                dbc.Col(xs=3,children=[
                      html.H6("temperatuur:", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                      html.H5("16,9°C", className="text-meting"),
                ]), # einde col
                dbc.Col(xs=9,children=[

                        daq.GraduatedBar(
                                id='temperatuur-bar',
                                size = 400,
                                min=0, max=100,
                                step=2,
                                color={"ranges":{"green":[0,75],"yellow":[76,90],"red":[91,100]}},
                                value=10
                                ),

                ]), # einde col

            ]), # einde rij

            dbc.Row([

                dbc.Col(xs=3,children=[

                      html.H6("meterstand : ", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                      html.H5("54658 Nm³", className="text-meting"),

                ]), # einde col

                dbc.Col(xs=9,children=[



                ]), # einde col

            ]), # einde rij

        ]),
    ]

ODORISATIELabel = [

        dbc.CardHeader([html.H4("ODORISATIE")]),
        dbc.CardBody([

            dbc.Row([

                dbc.Col(xs=3,children=[
                      html.H6("inhoud : ", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                      html.H5("50 liter", className="text-meting"),
                ]), # einde col
                dbc.Col(xs=9,children=[

                        daq.Tank(
                                id='inhoud-odotank',
                                min=0, max=100,
                                width=400,
                                color='blue',
                                scale={'custom':{str(i):{'style':{'font-size': '12pt', 'font-family': 'Verdana','color':'yellow'},'label':str(i)} for i in range(0, 109)if i %10 ==0}},
                                units='liter',
                                value=50
                                ),

                ]), # einde col

            ]), # einde rij
            html.Br(),

            dbc.Row([

                dbc.Col(xs=3,children=[
                       html.H6("dosering:", className="text-subtitel", style=CARD_TEXT_STYLE_subtitel),
                       html.H5("12mg/Nm³", className="text-meting"),
                ]), # einde col
                dbc.Col(xs=9,children=[

                        daq.GraduatedBar(
                                id='dosering-bar',
                                size=400,
                                min=0, max=100,
                                step=2,
                                color={"ranges":{"green":[0,75],"yellow":[76,90],"red":[91,100]}},
                                style={'font-size': '14pt', 'font-family': 'Verdana','color':'black', 'font-weight': 'bold'},
                                showCurrentValue=True,
                                value=77,
                                ),

                ]), # einde col

            ]), # einde rij


        ]),
    ]



#GasKabineFoto = encode_jpgimage('assets/foto.jpg')



""" --------------------------------------------------------------"""
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


""" ********   ------ Layout --------  G A S   ***************************"""

Gas = dbc.Container(fluid=True, children=[
    ## Top

    html.H1('Gas',id="Titel",className='ml-1',style={'text-align': 'center', 'font-weight': 'bold', 'text-decoration': 'underline', 'color':'#33ccff'}),
    html.Br(),html.Br(),html.Br(),
    html.Br(),
    dbc.Row([
        ### Row 1, Kol 1
        dbc.Col(xl=4,xs=12,children=[

            html.Div([dcc.Graph(figure=gaskaart,id="GasKaart")])
        ]),
        ### ### Row 1, Kol 2
        dbc.Col(xl=4,xs=12,children=[
            html.Div([
                      html.Div(dbc.Card(GasKabineLabel, color="info", inverse=True)),
                      html.Br(),
                      html.Br()

                      ]),
                    html.Br(),
        ]),
        ### ### Row 1, Kol 2
        dbc.Col(xl=4,xs=12,children=[

            html.Img(src='data:image/jpg;base64,{}'.format(encodedjpg.decode()))

        ]),
    ]), # einde row 1
    dbc.Row([
        dbc.Col(xl=4,children=[

                        html.Div(id='dark_slider',style={'background-color': '#303030', 'color': 'yellow'},children=[
                            daq.DarkThemeProvider(theme=theme, children=[
                                daq.Slider(
                                        id='my-gauge-slider',
                                        color=theme['primary'],   # VERGEET deze niet om de kleur te veranderen !
                                        min=0,
                                        max=100,
                                        step=1,
                                        updatemode='drag',
                                        value=5
                                        )
                            ])
                        ]),

                        html.Div(id='dark_gauge',style={'display': 'block', 'background-color': '#303030', 'color': 'black'},children=[
                            daq.DarkThemeProvider(theme=theme, children=[
                                daq.Gauge(
                                        id='my-gauge',
                                        color={"gradient":True,"ranges":{"green":[0,50],"yellow":[50,80],"red":[80,100]}},
                                        value=2,
                                        label={'style':{'color':'yellow', 'font-size': '38pt'},'label':'ingangsdruk'},
                                        scale={
                                            'custom':{str(i):{'style':{'font-size': '14pt', 'font-family': 'Verdana','color':'brown'},'label':str(i)} for i in range(0, 109)if i %10 ==0}},
                                        max=100,
                                        min=0,
                                        ),
                            ])
                        ]), # einde div




        ]),  # einde kolom

        dbc.Col(xl=4, xs=12,children=[
                    html.Div([
                              html.Div(dbc.Card(EVHILabel, inverse=True, color="primary", outline=True)),
                              html.Br(),
                              html.Br()

                              ]),
                            html.Br(),
        ]),  # einde kolom

        dbc.Col(xl=4,xs=12,children=[
                    html.Div([
                            html.Div(dbc.Card(ODORISATIELabel, inverse=True, color="success", outline=True)),
                            html.Br(),
                            html.Br()

                    ])
        ]),  # einde kolom

   ]),
   dbc.Row([
            #html.Br(),html.Br(),
            dbc.Jumbotron(className='greyjumbotron',children=[
                            dbc.Container([

                                html.Img(id='image', src='children', height=800),

                                dbc.Button("Scenario", id="scenario-button", className="mr-2"),
                                html.Span(id='toggle-switch-output', children='0', style={'display': 'none'}), #verborgen lijn


                            ],
                            fluid=True,
                        )
            ],
            fluid=True,
            ) #end jumbotron
   ]),


])
#, style={'padding': '50px'}

#Gas= html.Div(id='page-inhoud', children=[daq.DarkThemeProvider(theme=theme, children=GasVervolg)])
    #,style={'border': 'solid 1px #A2B1C6', 'border-radius': '5px', 'padding': '50px', 'margin-top': '20px'})

@app.callback(
    Output('my-thermometer', 'value'),
    [Input('thermometer-slider', 'value')])
def update_thermometer(value):
    return value


@app.callback(
     Output('my-gauge', 'value'),
    [Input('my-gauge-slider', 'value')])
def updategauge(VWaarde):
    return VWaarde


@app.callback([
    Output('image', 'src'),
    Output('toggle-switch-output', 'children'),
    #Output('scenario-button','n_clicks')
    ],
        [Input('scenario-button', 'n_clicks')

        ])

def callback_image(Waarde):
    stand = html.H5('{}.'.format(Waarde))
    path = 'assets/'
    if not Waarde or Waarde % 8 == 0 :
        foto = encode_image(path+'GAS-afgekeurd-on-on.png')
    if Waarde % 8 == 1:
        foto = encode_image(path+'GAS-afgekeurd-off-on.png')
    if Waarde % 8 == 2:
        foto = encode_image(path+'GAS-afgekeurd-on-off.png')
    if Waarde % 8 == 3:
        foto = encode_image(path+'GAS-afgekeurd-off-off.png')
    if Waarde % 8 == 4:
        foto = encode_image(path+'GAS-net-on-on.png')
    if Waarde% 8 == 5:
        foto = encode_image(path+'GAS-net-on-off.png')
    if Waarde% 8  == 6:
        foto = encode_image(path+'GAS-net-off-on.png')
    if Waarde% 8  == 7:
        foto = encode_image(path+'GAS-net-off-off.png')
    return foto, stand




@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return Gas
    elif pathname == "/page-2":
        return html.P("pagina 2")
    elif pathname == "/page-3":
        return html.P("pagina 3")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )




if __name__ == '__main__':

    import os

    debug = False if os.environ['DASH_DEBUG_MODE'] == 'False' else True

    app.run_server(
        host='0.0.0.0',
        port=8050
)
