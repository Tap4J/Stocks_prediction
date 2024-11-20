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

    # Check if columns are single-level but incorrectly named
    if df1.columns[0] == ticker1:
        df1.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    if df2.columns[0] == ticker2:
        df2.columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']

    # Debug: Print to confirm
    print(f"Renamed columns for {ticker1}:\n", df1.columns)
    print(f"Renamed columns for {ticker2}:\n", df2.columns)
    return df1, df2


def update_plot(data, indicators, ticker, sync_axis=None):
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

    # Plot indicators if specified
    for indicator in indicators:
        if indicator == "30 Day SMA":
            data['SMA30'] = data[close_col].rolling(30).mean()
            p.line(data.index, data['SMA30'], color="purple", legend_label="30 Day SMA")
        elif indicator == "100 Day SMA":
            data['SMA100'] = data[close_col].rolling(100).mean()
            p.line(data.index, data['SMA100'], color="blue", legend_label="100 Day SMA")
        elif indicator == "Linear Regression Line":
            x_vals = np.arange(len(data.index))
            y_vals = data[close_col].values
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            y_predicted = slope * x_vals + intercept
            p.line(data.index, y_predicted, legend_label="Linear Regression", color="red")

    # Add legend properties after glyphs are created
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"

    return p

def on_button_click(main_stock, comparison_stock, start, end, indicators):
    source1, source2 = load_data(main_stock, comparison_stock, start, end)

    if source1.empty or source2.empty:
        print("One or both data sources are empty. Check stock tickers and date range.")
        return

    p = update_plot(source1, indicators, source1.columns[0], )
    print(source1)
    p2 = update_plot(source2, indicators, source2.columns[0], sync_axis=p.x_range)

    updated_layout = column(layout, row(p, p2))
    curdoc().clear()
    curdoc().add_root(updated_layout)


stock1_text = TextInput(title="Main Stock", value="TSLA")
stock2_text = TextInput(title="Comparison Stock", value="AAPL")
date_picker_from = DatePicker(title='Start Date', value="2024-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title='End Date', value="2024-02-02", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"])

load_button = Button(label="Load Data", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, indicator_choice.value))

layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)

curdoc().clear()
curdoc().add_root(layout)