import dash
from dash import html
import pandas as pd

from config import DATA_PATH
from data_loader import load_data
from layout import create_layout
from callbacks import register_callbacks

df = load_data()

app = dash.Dash(__name__, title="Анализ успеваемости студентов")
server = app.server

app.layout = create_layout()

register_callbacks(app, df)

if __name__ == '__main__':
    app.run(debug=True)