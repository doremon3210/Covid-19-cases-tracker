from __future__ import annotations
from matplotlib.pyplot import annotate
import requests
import pandas as pd
import pycountry 
import plotly.express as px

URL = requests.get("https://www.worldometers.info/coronavirus/#main_table")
df = pd.read_html(URL.text, displayed_only=False)

def Select_data(choice):
    df = df[choice]