# spacex_dash_app.py

import os
import pandas as pd
import dash
import wget
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# -------------------------
# Load data
# -------------------------
DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
CSV_NAME = "spacex_launch_dash.csv"

if not os.path.exists(CSV_NAME):
    wget.download(DATA_URL, CSV_NAME)

spacex_df = pd.read_csv(CSV_NAME)

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# -------------------------
# Dash app
# -------------------------
app = dash.Dash(__name__)

# Dropdown options (include ALL)
launch_sites = sorted(spacex_df['Launch Site'].unique())
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in launch_sites
]

app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: RangeSlider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}
    ),
    html.Br(),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# -------------------------
# TASK 2 callback: Pie chart
# -------------------------
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Total success launches count (sum of class) for each site
        df_success = spacex_df.groupby('Launch Site', as_index=False)['class'].sum()
        fig = px.pie(
            df_success,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site'
        )
        return fig
    else:
        # Success vs Failure for selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        outcome_counts = site_df['class'].value_counts().reset_index()
        outcome_counts.columns = ['class', 'count']
        outcome_counts['Outcome'] = outcome_counts['class'].map({1: 'Success', 0: 'Failure'})

        fig = px.pie(
            outcome_counts,
            values='count',
            names='Outcome',
            title=f'Total Success vs Failure for site {entered_site}'
        )
        return fig

# -------------------------
# TASK 4 callback: Scatter chart
# -------------------------
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range

    # filter by payload range first
    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == entered_site]
        title = f'Correlation between Payload and Success for site {entered_site}'
    else:
        title = 'Correlation between Payload and Success for all sites'

    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=title
    )
    return fig

# -------------------------
# Run
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)
