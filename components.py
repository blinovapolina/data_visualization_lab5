# components.py
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

GRADE_ORDER = ['a', 'b', 'c', 'd', 'e', 'f']
TRAVEL_ORDER = ['<15 min', '15-30 min', '30-60 min', '>60 min']

GRADE_COLORS = {
    'a': '#27ae60',
    'b': '#2ecc71',
    'c': '#f1c40f',
    'd': '#e67e22',
    'e': '#e74c3c',
    'f': '#c0392b'
}

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

def create_internet_extra_heatmap(dff):
    """Тепловая карта: влияние интернета и доп. занятий"""
    pivot_df = dff.pivot_table(
        values='overall_score', 
        index='internet_access', 
        columns='extra_activities', 
        aggfunc='mean'
    ).fillna(0)
    
    fig = px.imshow(
        pivot_df.values,
        x=pivot_df.columns,
        y=pivot_df.index,
        labels=dict(x="Дополнительные занятия", y="Доступ к интернету", color="Средний балл"),
        title="Тепловая карта: средний балл в зависимости от интернета и доп. занятий",
        color_continuous_scale='Viridis',
        aspect="auto",
        text_auto='.2f'
    )
    fig.update_layout(height=400)
    return fig

def create_extra_activities_chart(dff):
    """Группированная столбчатая диаграмма: распределение оценок по доп. занятиям"""
    grade_dist = dff.groupby(['extra_activities', 'final_grade']).size().reset_index(name='count')
    total_by_group = grade_dist.groupby('extra_activities')['count'].sum().reset_index(name='total')
    grade_dist = grade_dist.merge(total_by_group, on='extra_activities')
    grade_dist['percent'] = grade_dist['count'] / grade_dist['total'] * 100
    grade_dist['final_grade_numeric'] = grade_dist['final_grade'].map({'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1, 'f': 0})
    
    fig = px.bar(
        grade_dist, 
        x='final_grade_numeric', 
        y='percent', 
        color='extra_activities',
        barmode='group',
        title='Распределение оценок: сравнение групп с дополнительными занятиями и без',
        labels={'final_grade_numeric': 'Числовая оценка (0-5)', 'percent': 'Процент студентов', 'extra_activities': 'Дополнительные занятия'},
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto='.1f'
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