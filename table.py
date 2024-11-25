import numpy as np
import math
import pandas as pd
import yfinance as yf
import datetime as dt

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, TableColumn, StringFormatter

def fetch_top_tickers():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BABA', 'AMD']
    return tickers

def create_ticker_table(tickers):
    tickers_data = pd.DataFrame(tickers, columns=['Ticker'])
    source = ColumnDataSource(tickers_data)
    columns = [TableColumn(field="Ticker", title="Available Tickers", formatter=StringFormatter())]
    data_table = DataTable(source=source, columns=columns, width=200, height=280)
    return data_table

top_tickers = fetch_top_tickers()
ticker_table = create_ticker_table(top_tickers)

layout = column(ticker_table)
curdoc().add_root(layout)
