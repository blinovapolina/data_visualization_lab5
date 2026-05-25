from dash import Input, Output
import pandas as pd
from data_loader import filter_data, get_kpi_data
from components import (
    create_kpi_card, create_grade_histogram, create_study_hours_boxplot,
    create_attendance_violin, create_internet_extra_chart,
    create_parent_education_chart, create_travel_time_chart
)
from config import COLORS

def register_callbacks(app, df):
    """Регистрация всех callback-функций"""
    
    @app.callback(
        [Output('school-filter', 'options'),
         Output('internet-filter', 'options'),
         Output('extra-filter', 'options')],
        [Input('school-filter', 'id')]
    )
    def init_filters(_):
        school_options = [{'label': 'Все', 'value': 'all'}] + \
                         [{'label': i, 'value': i} for i in df['school_type'].unique()]
        internet_options = [{'label': 'Все', 'value': 'all'}] + \
                           [{'label': i, 'value': i} for i in df['internet_access'].unique()]
        extra_options = [{'label': 'Все', 'value': 'all'}] + \
                        [{'label': i, 'value': i} for i in df['extra_activities'].unique()]
        return school_options, internet_options, extra_options
    
    @app.callback(
        [Output('kpi-container', 'children'),
         Output('grade-histogram', 'figure'),
         Output('study-hours-boxplot', 'figure'),
         Output('attendance-violin', 'figure'),
         Output('internet-extra-bar', 'figure'),
         Output('parent-edu-bar', 'figure'),
         Output('travel-boxplot', 'figure')],
        [Input('school-filter', 'value'),
         Input('internet-filter', 'value'),
         Input('extra-filter', 'value')]
    )
    def update_dashboard(school, internet, extra):
        dff = filter_data(df, school, internet, extra)
        kpi = get_kpi_data(dff)
        
        kpi_cards = [
            create_kpi_card("Средняя оценка", f"{kpi['avg_grade']:.2f}", COLORS['success'], ""),
            create_kpi_card("Средняя посещаемость", f"{kpi['avg_attendance']:.1f}%", COLORS['info'], ""),
            create_kpi_card("Часов учебы/день", f"{kpi['avg_study_hours']:.1f}", COLORS['warning'], ""),
            create_kpi_card("Всего студентов", f"{kpi['total_students']}", COLORS['purple'], "")
        ]
        
        fig_hist = create_grade_histogram(dff)
        fig_box = create_study_hours_boxplot(dff)
        fig_violin = create_attendance_violin(dff)
        fig_bar = create_internet_extra_chart(dff)
        fig_parent = create_parent_education_chart(dff)
        fig_travel = create_travel_time_chart(dff)
        
        return kpi_cards, fig_hist, fig_box, fig_violin, fig_bar, fig_parent, fig_travel
    
    @app.callback(
        [Output('school-filter', 'value'),
         Output('internet-filter', 'value'),
         Output('extra-filter', 'value')],
        [Input('school-filter', 'options')]
    )
    def set_default_values(_):
        return 'all', 'all', 'all'