from dash import dcc, html
from config import COLORS

def create_layout():
    """Создание макета дашборда"""
    return html.Div([
        html.Div([
            html.H1("Анализ факторов успеваемости студентов", 
                    style={'textAlign': 'center', 'color': COLORS['primary'], 'marginBottom': 20}),
            html.P("Исследование влияния различных факторов на академическую успеваемость",
                   style={'textAlign': 'center', 'color': '#666', 'marginBottom': 30})
        ]),
        
        html.Div(id='kpi-container', className="row", style={'marginBottom': 30}),
        
        html.Div([
            html.Div([
                html.Label("Тип школы:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='school-filter', clearable=False)
            ], className="four columns"),
            
            html.Div([
                html.Label("Доступ к интернету:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='internet-filter', clearable=False)
            ], className="four columns"),
            
            html.Div([
                html.Label("Дополнительные занятия:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(id='extra-filter', clearable=False)
            ], className="four columns"),
        ], className="row", style={'marginBottom': 30}),
        
        html.Div([
            html.Div([dcc.Graph(id='grade-histogram')], className="six columns"),
            html.Div([dcc.Graph(id='study-hours-boxplot')], className="six columns"),
        ], className="row"),
        
        html.Div([
            html.Div([dcc.Graph(id='attendance-violin')], className="six columns"),
            html.Div([dcc.Graph(id='internet-extra-bar')], className="six columns"),
        ], className="row", style={'marginTop': 20}),
        
        html.Div([
            html.Div([dcc.Graph(id='parent-edu-bar')], className="six columns"),
            html.Div([dcc.Graph(id='travel-boxplot')], className="six columns"),
        ], className="row", style={'marginTop': 20}),
        
        html.Hr(),
        html.P("2024 - Анализ успеваемости студентов | Данные: Student Performance Dataset",
               style={'textAlign': 'center', 'color': '#999', 'fontSize': '12px', 'marginTop': 30})
        
    ], style={'maxWidth': '1400px', 'margin': '0 auto', 'padding': '20px'})