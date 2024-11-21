import numpy as np
import math
import pandas as pd
import yfinance as yf
import datetime as dt

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, MultiChoice

def load_data(ticker1, ticker2, start, end):
    df1 = yf.download(ticker1, start=start, end=end)
    df2 = yf.download(ticker2, start=start, end=end)

    #I need to rename columns (multindex)
    df1 = df1.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    df2 = df2.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    
    return df1, df2

def update_plot(data, ticker, indicators, sync_axis=None):
    if data.empty:
        print("Data is empty, no plot will be generated.")
        return figure()

    # Print columns to verify structure. Normally I would delete, but keeping to see how I approached
    print(f"Columns in the DataFrame: {data.columns}")

    # Extraction for ticker
    close_col = ('Close', ticker)
    open_col = ('Open', ticker)
    high_col = ('High', ticker)
    low_col = ('Low', ticker)

    # Check if existing
    if not {close_col, open_col, high_col, low_col}.issubset(data.columns):
        print(f"Data does not have the required columns for {ticker}.")
        print(f"Expected columns: {close_col}, {open_col}, {high_col}, {low_col}")
        return figure()

    gain = data[close_col] > data[open_col]
    loss = data[open_col] > data[close_col]
    width = 12 * 60 * 60 * 1000 # 12 hours in ms

    # Create figure
    if sync_axis is not None:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000, x_range=sync_axis)
    else:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.3

    # Plot the data
    p.segment(data.index, data[high_col], data.index, data[low_col], color="black", legend_label="High-Low")
    p.vbar(data.index[gain], width, data[open_col][gain], data[close_col][gain], fill_color="#00ff00", line_color="#00ff00", legend_label="Gain")
    p.vbar(data.index[loss], width, data[open_col][loss], data[close_col][loss], fill_color="#ff0000", line_color="#ff0000", legend_label="Loss")
    
    # Definition fot indicators
    for indicator in indicators:
        print(indicator)
        if indicator== "30 Day SMA":
            data['SMA30'] = data['Close'].rolling(window=30).mean()
            p.line(data.index, data['SMA30'], color="purple", legend_label="30 Day SMA")

        elif indicator== "100 Day SMA":
            data['SMA100'] = data['Close'].rolling(window=100).mean()
            p.line(data.index, data['SMA100'], color="orange", legend_label="100 Day SMA")


        elif indicator== "Linear Regression Line":
            x_vals = np.arange(len(data.index))
            y_vals = data['Close'].values
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            y_predicted = slope * x_vals + intercept
            p.line(data.index, y_predicted, legend_label="Linear Regression", color="red")


    return p


def on_button_click(main_stock, comparison_stock, start, end, indicators):
    try:
        # Loading data for first ticker and second ticker, adding dates
        df1, df2 = load_data(main_stock, comparison_stock, start, end)
        if df1.empty or df2.empty:
            print("One or both data sources are empty. Check stock tickers and date range.")
            return
        
        # Call function for plot
        p = update_plot(df1, main_stock, indicators)
        p2 = update_plot(df2, comparison_stock, indicators)

        updated_layout = column(layout, row(p, p2))
        curdoc().clear()
        curdoc().add_root(updated_layout)
    except Exception as e:
       print(f"Error: {e}")

stock1_text = TextInput(title="Main Stock", value='TSLA')
stock2_text = TextInput(title="Comparison Stock", value='AAPL')
date_picker_from = DatePicker(title='Start Date', value="2024-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title='End Date', value="2024-02-02", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"])

load_button = Button(label="Load Data", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, indicator_choice.value))
layout=column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().clear()
curdoc().add_root(layout)