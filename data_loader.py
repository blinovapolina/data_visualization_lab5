import pandas as pd
from config import DATA_PATH

def load_data():
    """Загрузка и подготовка данных"""
    df = pd.read_csv(DATA_PATH)
    
    df['final_grade'] = df['final_grade'].str.lower()
    grade_mapping = {'a': 5, 'b': 4, 'c': 3, 'd': 2, 'e': 1, 'f': 0}
    df['final_grade_numeric'] = df['final_grade'].map(grade_mapping)
    
    travel_mapping = {'<15 min': 1, '15-30 min': 2, '30-60 min': 3, '>60 min': 4}
    df['travel_numeric'] = df['travel_time'].map(travel_mapping)
    
    return df

def filter_data(df, school, internet, extra):
    dff = df.copy()
    if school and school != 'all':
        dff = dff[dff['school_type'] == school]
    if internet and internet != 'all':
        dff = dff[dff['internet_access'] == internet]
    if extra and extra != 'all':
        dff = dff[dff['extra_activities'] == extra]
    return dff

def get_kpi_data(dff):
    return {
        'avg_grade': dff['final_grade_numeric'].mean(),
        'avg_attendance': dff['attendance_percentage'].mean(),
        'avg_study_hours': dff['study_hours'].mean(),
        'total_students': len(dff)
    }