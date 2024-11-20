import math
import datetime as dt
import pandas as pd

import numpy as np
import yfinance as yf

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import TextInput, Button, DatePicker, MultiChoice

def load_data(ticker1, ticker2, start, end):
    # Download data
    df1 = yf.download(ticker1, start=start, end=end)
    df2 = yf.download(ticker2, start=start, end=end)

    df1 = df1.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})

    df2 = df2.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    return df1, df2

def update_plot(data, ticker, sync_axis=None):
    if data.empty:
        print("Data is empty, no plot will be generated.")
        return figure()

    # Debugging: Print column names to verify structure
    print(f"Columns in the DataFrame: {data.columns}")

    # Extracting columns for the specific ticker
    close_col = ('Close', ticker)
    open_col = ('Open', ticker)
    high_col = ('High', ticker)
    low_col = ('Low', ticker)

    # Ensure the required columns exist
    if not {close_col, open_col, high_col, low_col}.issubset(data.columns):
        print(f"Data does not have the required columns for {ticker}.")
        print(f"Expected columns: {close_col}, {open_col}, {high_col}, {low_col}")
        return figure()

    # Compute gain and loss masks
    gain = data[close_col] > data[open_col]
    loss = ~gain
    width = 12 * 60 * 60 * 1000  # half day in ms

    # Create figure with optional synced x-axis
    if sync_axis is not None:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000, x_range=sync_axis)
    else:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.3

    # Plot the data with legend_label to enable legend
    p.segment(data.index, data[high_col], data.index, data[low_col], color="black", legend_label="High-Low")
    p.vbar(data.index[gain], width, data[open_col][gain], data[close_col][gain], fill_color="#00ff00", line_color="#00ff00", legend_label="Gain")
    p.vbar(data.index[loss], width, data[open_col][loss], data[close_col][loss], fill_color="#ff0000", line_color="#ff0000", legend_label="Loss")

    return p


def on_button_click(main_stock, comparison_stock, start, end):
    df1, df2 = load_data(main_stock, comparison_stock, start, end)
    print(df1)

    if df1.empty or df2.empty:
        print("One or both data sources are empty. Check stock tickers and date range.")
        return

    p = update_plot(df1, main_stock)
    print(df1)
    p2 = update_plot(df2, comparison_stock)

    updated_layout = column(layout, row(p, p2))
    curdoc().clear()
    curdoc().add_root(updated_layout)



stock1_text = TextInput(title="Main Stock", value='TSLA')
stock2_text = TextInput(title="Comparison Stock", value='AAPL')
date_picker_from = DatePicker(title='Start Date', value="2024-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title='End Date', value="2024-02-02", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))



load_button = Button(label="Load Data", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, ))

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to,load_button)

curdoc().clear()
curdoc().add_root(layout)



















