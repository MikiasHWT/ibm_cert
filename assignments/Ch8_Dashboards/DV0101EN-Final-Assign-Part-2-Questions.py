#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
year_list = [i for i in range(1980, 2024)]

# Layout
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'text-align': 'center', 'color': '#503D36', 'font-size': '24px'}
    ),
    html.Div([
        html.Label("Select Statistics:", style={'font-size': '20px'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Yearly Statistics',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center'
            }
        )
    ], style={'margin-bottom': '20px'}),
    html.Div([
        html.Label("Select Year:", style={'font-size': '20px'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            value=None,
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center'
            }
        )
    ], style={'margin-bottom': '20px'}),
    html.Div([
        html.Div(
            id='output-container',
            className='chart-grid',
            style={'display': 'flex'}
        )
    ])
])

# Callback to enable/disable year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    return selected_statistics != 'Yearly Statistics'

# Callback to generate plots
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter for recession data
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile Sales Fluctuation
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(
            yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales Fluctuation Over Recession Period"
        ))

        # Plot 2: Average Vehicles Sold by Vehicle Type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            avg_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type (Recession)"
        ))

        # Plot 3: Advertising Expenditure Share by Vehicle Type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
            title="Total Advertising Expenditure Share by Vehicle Type (Recession)"
        ))

        # Plot 4: Unemployment Rate Effect on Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(
            unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
            title="Effect of Unemployment Rate on Vehicle Type and Sales"
        ))

        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter for selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Average Automobile Sales
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas, x='Year', y='Automobile_Sales', title="Yearly Average Automobile Sales"
        ))

        # Plot 2: Monthly Automobile Sales
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(
            mas, x='Month', y='Automobile_Sales', title=f"Total Monthly Automobile Sales in {input_year}"
        ))

        # Plot 3: Average Vehicles Sold by Vehicle Type
        avg_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avg_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f"Average Vehicles Sold by Vehicle Type in {input_year}"
        ))

        # Plot 4: Advertising Expenditure by Vehicle Type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
            title=f"Total Advertising Expenditure by Vehicle Type in {input_year}"
        ))

        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    return None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
