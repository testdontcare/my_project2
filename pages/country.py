from dash import html, dcc, callback, Output, Input, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

all_cont = df['continent'].unique()

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3("Подробная информация о выбранной стране"),
                html.Hr(style={'color': 'black'}),
            ], style={'textAlign': 'center'})
        )
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P("Выберите континент:")
        ], width=2),
        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-cont',
                options=[{'label': i, 'value': i} for i in all_cont],
                value=all_cont[0],
                multi=False
            )
        ], width=3),
        dbc.Col([
            html.P("Выберите страну:")
        ], width=2),
        dbc.Col([
            dcc.Dropdown(
                id='crossfilter-count',
                multi=False
            )
        ], width=3)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Уровень жизни (лет)"),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/money.png')
                    ], width=4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                                id='card_text1',
                                className="card-value"
                            ),
                        )
                    ], width=8),
                ])
            ], color="success", outline=True, style={'textAlign': 'center'}),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Численность населения (млн)"),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/religious.png')
                    ], width=4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                                id='card_text2',
                                className="card-value"
                            ),
                        )
                    ], width=8),
                ])
            ], color="danger", outline=True, style={'textAlign': 'center'}),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Образование (лет)"),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/diploma.png')
                    ], width=4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                                id='card_text3',
                                className="card-value"
                            ),
                        )
                    ], width=8),
                ])
            ], color="primary", outline=True, style={'textAlign': 'center'}),
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Статус"),
                dbc.Row([
                    dbc.Col([
                        dbc.CardImg(src='/static/images/globe.png')
                    ], width=4),
                    dbc.Col([
                        dbc.CardBody(
                            html.P(
                                id='card_text4',
                                className="card-value"
                            ),
                        )
                    ], width=8),
                ])
            ], color="info", outline=True, style={'textAlign': 'center'}),
        ], width=3),
    ]),

    html.Br(),

    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Уровень ВВП по странам континента на 2015 год"),
                dcc.Graph(id='choropleth'),
            ], width=8),
            dbc.Col([
                dbc.Row([
                    html.Div(id="card1")
                ]),
                html.Br(),
                dbc.Row([
                    html.H5("ТОП-5 стран по ВВП"),
                    html.Div(id="Label1"),
                ], style={'textAlign': 'center'})
            ], width=4)
        ], style={'textAlign': 'center'}),
    ])
])

def update_region(cont):
    all_count = df[df['continent'] == cont]['Country'].unique()
    dd_count = [{'label': i, 'value': i} for i in all_count]
    dd_count_value = all_count[0] if all_count.size > 0 else None
    return dd_count, dd_count_value

@callback(
    [Output('card_text1', 'children'),
     Output('card_text2', 'children'),
     Output('card_text3', 'children'),
     Output('card_text4', 'children'),
     Output('card1', 'children'),
     Output('Label1', 'children'),
     Output('choropleth', 'figure')],
    [Input('crossfilter-count', 'value'),
     Input('crossfilter-cont', 'value')]
)
def update_card(count, cont):
    df_count = df[(df['Country'] == count) & (df['Year'] == 2015)]
    df_count14 = df[(df['Country'] == count) & (df['Year'] == 2014)]
    gdp_count = df[(df['continent'] == cont) & (df['Year'] == 2015)].sort_values(by='GDP', ascending=False)

    if df_count.empty or df_count14.empty:
        return "N/A", "N/A", "N/A", "N/A", "", "", px.Figure()

    ct1 = f"{df_count.iloc[0]['Life expectancy']} лет"
    ct2 = f"{df_count.iloc[0]['Population'] / 1e6:.2f} млн"
    ct3 = f"{df_count.iloc[0]['Schooling']} лет"
    ct4 = df_count.iloc[0]['Status']
    gdp15 = df_count.iloc[0]['GDP']
    gdp14 = df_count14.iloc[0]['GDP']
    gdp_table = gdp_count.iloc[0:5][['Country', 'GDP']]
    delta_gdp = round((gdp15 - gdp14) / gdp14, 2) * 100

    card1 = dbc.Card([
        dbc.CardHeader("Валовый внутренний продукт (ВВП)"),
        dbc.CardBody([
            html.H5(f"{gdp15:,.2f}"),
            html.Div([
                html.I(f"{delta_gdp}%"),
                html.Span(' в % к 2014 году')
            ])
        ])
    ], style={'textAlign': 'center'})

    table = dbc.Table.from_dataframe(gdp_table, striped=True, bordered=True, hover=True, index=False)

    figure = px.choropleth(
        gdp_count,
        locations='Country',
        locationmode='country names',
        color="GDP",
        hover_name='Country',
        hover_data={'Country': True, 'Year': False, 'Status': False,
                    'Life expectancy': True, 'Population': True,
                    'GDP': True, 'Schooling': False,
                    'continent': False},
        labels={'Country': 'Страна', 'Year': 'Год',
                'Population': 'Население', 'Life expectancy': 'Продолжительность жизни',
                'GDP': 'ВВП', 'Schooling': 'Продолжительность обучения'},
        color_continuous_scale=px.colors.sequential.Teal,
    )

    figure.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                         showlegend=False,
                         coloraxis_showscale=False)

    return ct1, ct2, ct3, ct4, card1, table, figure
