from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
from data import df

all_continents = df['continent'].unique()
min_year = df['Year'].min()
max_year = df['Year'].max()

layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H3("Статистика по континентам и временным интервалам"),
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
                id='continent-filter',
                options=[{'label': cont, 'value': cont} for cont in all_continents],
                value=all_continents[0],
                multi=False
            )
        ], width=4),
        dbc.Col([
            html.P("Выберите временной интервал:")
        ], width=2),
        dbc.Col([
            dcc.DatePickerRange(
                id='date-range',
                start_date=f"{min_year}-01-01",
                end_date=f"{max_year}-12-31",
                display_format='YYYY-MM-DD',
                min_date_allowed=f"{min_year}-01-01",
                max_date_allowed=f"{max_year}-12-31"
            )
        ], width=4)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='life-expectancy-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='population-graph')
        ], width=6)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='gdp-graph')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='schooling-graph')
        ], width=6)
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='status-graph')
        ], width=12)
    ]),
])

@callback(
    [Output('life-expectancy-graph', 'figure'),
     Output('population-graph', 'figure'),
     Output('gdp-graph', 'figure'),
     Output('schooling-graph', 'figure'),
     Output('status-graph', 'figure')],
    [Input('continent-filter', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date')]
)
def update_graphs(continent, start_date, end_date):
    start_year = int(start_date.split('-')[0])
    end_year = int(end_date.split('-')[0])
    
    filtered_df = df[(df['continent'] == continent) & 
                     (df['Year'] >= start_year) & 
                     (df['Year'] <= end_year)]
    
    life_expectancy_fig = px.line(filtered_df, x='Year', y='Life expectancy', 
                                  title='Продолжительность жизни', 
                                  labels={'Life expectancy': 'Продолжительность жизни', 'Year': 'Год'},
                                  color='Country')
    
    population_fig = px.line(filtered_df, x='Year', y='Population', 
                             title='Численность населения', 
                             labels={'Population': 'Население', 'Year': 'Год'},
                             color='Country')
    
    gdp_fig = px.line(filtered_df, x='Year', y='GDP', 
                      title='ВВП', 
                      labels={'GDP': 'ВВП', 'Year': 'Год'},
                      color='Country')
    
    schooling_fig = px.line(filtered_df, x='Year', y='Schooling', 
                            title='Образование', 
                            labels={'Schooling': 'Образование', 'Year': 'Год'},
                            color='Country')
    
    status_fig = px.scatter(filtered_df, x='Year', y='Status', 
                            title='Статус', 
                            labels={'Status': 'Статус', 'Year': 'Год'},
                            color='Country',
                            size='Population',
                            hover_name='Country')

    return life_expectancy_fig, population_fig, gdp_fig, schooling_fig, status_fig