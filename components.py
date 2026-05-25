# components.py
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from config import COLORS, GRADE_ORDER, TRAVEL_ORDER, GRADE_COLORS

def create_kpi_card(title, value, color, icon=""):
    """Создание карточки с KPI"""
    return html.Div([
        html.Div([
            html.H3(f"{icon} {title}".strip(), style={'margin': 0, 'color': '#555', 'fontSize': '14px'}),
            html.H2(value, style={'margin': '10px 0', 'color': color, 'fontWeight': 'bold'})
        ], style={
            'textAlign': 'center', 
            'padding': '15px', 
            'backgroundColor': COLORS['background'], 
            'borderRadius': '10px', 
            'boxShadow': '2px 2px 5px rgba(0,0,0,0.1)',
            'borderLeft': f'4px solid {color}'
        })
    ], className="three columns")

def create_grade_histogram(dff):
    """Гистограмма распределения оценок"""
    grade_counts = dff['final_grade'].value_counts().reindex(GRADE_ORDER, fill_value=0)
    fig = px.bar(
        x=grade_counts.index, y=grade_counts.values,
        labels={'x': 'Итоговая оценка', 'y': 'Количество студентов'},
        title='Распределение итоговых оценок',
        color=grade_counts.index,
        color_discrete_map=GRADE_COLORS,
        text_auto=True
    )
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_study_hours_boxplot(dff):
    """Ящик с усами: часы учебы vs оценка"""
    fig = px.box(
        dff, x='final_grade', y='study_hours', color='final_grade',
        title='Часы учебы в день по оценкам',
        labels={'final_grade': 'Оценка', 'study_hours': 'Часы учебы'},
        category_orders={'final_grade': GRADE_ORDER},
        color_discrete_map=GRADE_COLORS
    )
    fig.update_layout(showlegend=False, height=400)
    return fig

def create_attendance_violin(dff):
    """Скрипичный график посещаемости"""
    fig = go.Figure()
    for grade in GRADE_ORDER:
        subset = dff[dff['final_grade'] == grade]['attendance_percentage']
        if len(subset) > 0:
            fig.add_trace(go.Violin(
                x=[grade.upper()] * len(subset),
                y=subset,
                name=grade.upper(),
                box_visible=True,
                meanline_visible=True,
                fillcolor=GRADE_COLORS.get(grade, '#3498db')
            ))
    fig.update_layout(
        title='Плотность распределения посещаемости по оценкам',
        xaxis_title='Оценка',
        yaxis_title='Процент посещаемости (%)',
        height=400
    )
    return fig

def create_internet_extra_chart(dff):
    """Влияние интернета и доп. занятий"""
    pivot_df = dff.pivot_table(
        values='overall_score', 
        index='internet_access', 
        columns='extra_activities', 
        aggfunc='mean'
    ).fillna(0)
    pivot_melted = pivot_df.reset_index().melt(
        id_vars='internet_access', 
        var_name='extra_activities', 
        value_name='overall_score'
    )
    fig = px.bar(
        pivot_melted, x='internet_access', y='overall_score', color='extra_activities',
        barmode='group',
        title='Влияние интернета и доп. занятий на успеваемость',
        labels={'internet_access': 'Доступ к интернету', 'overall_score': 'Средний балл', 'extra_activities': 'Доп. занятия'},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(height=400)
    return fig

def create_parent_education_chart(dff):
    """Образование родителей vs успеваемость"""
    parent_means = dff.groupby('parent_education')['final_grade_numeric'].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        parent_means, x='parent_education', y='final_grade_numeric',
        title='Образование родителей и успеваемость',
        labels={'parent_education': 'Образование родителей', 'final_grade_numeric': 'Средняя оценка'},
        color='final_grade_numeric',
        color_continuous_scale='Blues',
        text_auto='.2f'
    )
    fig.update_layout(height=400)
    return fig

def create_travel_time_chart(dff):
    """Время в пути до школы"""
    fig = px.box(
        dff, x='travel_time', y='final_grade_numeric', color='travel_time',
        title='Время в пути до школы vs Успеваемость',
        labels={'travel_time': 'Время в пути', 'final_grade_numeric': 'Числовая оценка (0-5)'},
        category_orders={'travel_time': TRAVEL_ORDER},
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_layout(showlegend=False, height=400)
    return fig