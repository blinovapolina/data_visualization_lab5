from flask import Flask, render_template
import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components import (
    create_grade_histogram, create_study_hours_boxplot,
    create_attendance_violin, create_internet_extra_heatmap,
    create_extra_activities_chart, create_parent_education_chart
)
from data_loader import load_data, get_kpi_data

df = load_data()

kpi_data = get_kpi_data(df)

fig_parent = create_parent_education_chart(df)

# Тепловая карта: интернет и доп. занятия
fig_internet_extra_heatmap = create_internet_extra_heatmap(df)

# Группированная столбчатая диаграмма: распределение оценок по доп. занятиям
fig_extra_activities = create_extra_activities_chart(df)

df_display = df.head(100).copy()
df_display = df_display.drop(columns=['student_id', 'travel_numeric'], errors='ignore')



server = Flask(__name__)

@server.route('/')
def index():
    return render_template("index.html")


dash_data_app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/data/',
    suppress_callback_exceptions=True
)

dash_data_app.layout = html.Div(style={
    'fontFamily': 'Sans-serif',
    'textAlign': 'center',
    'padding': '10px',
    'backgroundColor': '#f0f8ff'
}, children=[
    html.H2("Исходные данные об успеваемости студентов"),
    html.A("Назад", href='/', style={
        'color': '#28a745',
        'textDecoration': 'none',
        'fontSize': '1.1em',
        'marginBottom': '20px',
        'display': 'inline-block'
    }),
    dash_table.DataTable(
        data=df_display.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df_display.columns],
        style_cell={'textAlign': 'center', 'padding': '5px'},
        style_header={
            'backgroundColor': '#28a745',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_table={'width': '100%', 'margin': '0 auto', 'marginTop': '10px', 'overflowX': 'auto'}
    ),
])


dash_dashboard_app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/dashboard/',
    suppress_callback_exceptions=True
)

dash_dashboard_app.layout = html.Div(style={
    'fontFamily': 'Sans-serif',
    'textAlign': 'center',
    'padding': '10px',
    'backgroundColor': '#f0f8ff'
}, children=[
    html.H2("Аналитика успеваемости студентов"),
    html.A("Назад", href='/', style={
        'color': '#28a745',
        'textDecoration': 'none',
        'fontSize': '1.1em',
        'marginBottom': '20px',
        'display': 'inline-block'
    }),
    
    html.Div([
        html.Div([
            html.Div([
                html.H3("Средняя оценка", style={'margin': 0, 'color': '#555'}),
                html.H2(f"{kpi_data['avg_grade']:.2f}", style={'margin': '10px 0', 'color': '#27ae60'})
            ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 
                      'borderRadius': '10px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'})
        ], className="three columns", style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H3("Средняя посещаемость", style={'margin': 0, 'color': '#555'}),
                html.H2(f"{kpi_data['avg_attendance']:.1f}%", style={'margin': '10px 0', 'color': '#2980b9'})
            ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 
                      'borderRadius': '10px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'})
        ], className="three columns", style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H3("Часов учебы/день", style={'margin': 0, 'color': '#555'}),
                html.H2(f"{kpi_data['avg_study_hours']:.1f}", style={'margin': '10px 0', 'color': '#e67e22'})
            ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 
                      'borderRadius': '10px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'})
        ], className="three columns", style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H3("Всего студентов", style={'margin': 0, 'color': '#555'}),
                html.H2(f"{kpi_data['total_students']}", style={'margin': '10px 0', 'color': '#8e44ad'})
            ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': '#f8f9fa', 
                      'borderRadius': '10px', 'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)'})
        ], className="three columns", style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
    ], style={'marginBottom': '20px'}),
    
    dcc.Tabs([
        dcc.Tab(label="Распределение оценок", children=[
            dcc.Graph(figure=create_grade_histogram(df), style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
        dcc.Tab(label="Часы учебы vs Оценка", children=[
            dcc.Graph(figure=create_study_hours_boxplot(df), style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
        dcc.Tab(label="Посещаемость vs Оценка", children=[
            dcc.Graph(figure=create_attendance_violin(df), style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
        dcc.Tab(label="Образование родителей", children=[
            dcc.Graph(figure=fig_parent, style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
        dcc.Tab(label="Интернет и доп. занятия", children=[
            dcc.Graph(figure=fig_internet_extra_heatmap, style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
        dcc.Tab(label="Дополнительные занятия vs Оценки", children=[
            dcc.Graph(figure=fig_extra_activities, style={'marginBottom': '0px', 'marginTop': '0px'}),  
        ]),
    ], style={'marginTop': '10px', 'fontFamily': 'Sans-serif'}),
])


if __name__ == '__main__':
    server.run(debug=False, host='0.0.0.0', port=5001)