from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

from data import df_region, counties

rusmap = px.choropleth_mapbox(
                        df_region,
                        geojson=counties,
                        featureidkey='properties.cartodb_id',
                        color='ВВП на душу населения',
                        locations='cartodb_id',
                        color_continuous_scale=px.colors.sequential.Teal,
                        mapbox_style="carto-positron",
                        zoom=20,
                        # center = {'lat':55.755773, 'lon':37.617761},
                        opacity=0.5,
                        hover_name = 'region',
                        hover_data = {'region':True, 'cartodb_id':False},
                        labels={'region':'Субъект РФ'}
)
rusmap.update_layout(mapbox_style="carto-positron",
                        margin={"r":0,"t":0,"l":0,"b":0}, geo_scope='world',
                        mapbox_zoom=1, mapbox_center = {"lat": 66, "lon": 94}, height=500,
                        showlegend=False)

layout = dbc.Container([
    dbc.Row ([
        dbc.Col(
                html.Div([
                html.H3("Карта регионов Российской федерации"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),


    html.Br(),


    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=rusmap)
            ],width=12),
    ]),
])
