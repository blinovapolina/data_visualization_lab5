import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Student_Performance.csv')

GRADE_ORDER = ['a', 'b', 'c', 'd', 'e', 'f']
TRAVEL_ORDER = ['<15 min', '15-30 min', '30-60 min', '>60 min']

COLORS = {
    'primary': '#2c3e50',
    'success': '#27ae60',
    'info': '#2980b9',
    'warning': '#e67e22',
    'danger': '#e74c3c',
    'purple': '#8e44ad',
    'background': '#f8f9fa'
}

GRADE_COLORS = {
    'a': '#27ae60',
    'b': '#2ecc71',
    'c': '#f1c40f',
    'd': '#e67e22',
    'e': '#e74c3c',
    'f': '#c0392b'
}