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
    # Download data from yfinance
    df1 = yf.download(ticker1, start, end)
    df2 = yf.download(ticker2, start, end)

    # Print the raw data to inspect it
    print(f"Raw Data for {ticker1}:")
    print(df1.head())
    print(f"Raw Data for {ticker2}:")
    print(df2.head())

    # Flatten MultiIndex columns by combining ticker and field name properly
    print(f"Original Columns for {ticker1}: {df1.columns}")
    print(f"Original Columns for {ticker2}: {df2.columns}")

    # Flatten columns by joining the two levels in the MultiIndex correctly
    df1.columns = [f'{ticker1}_{col[0]}' for col in df1.columns]
    df2.columns = [f'{ticker2}_{col[0]}' for col in df2.columns]

    # Print the columns after flattening
    print(f"Flattened Columns for {ticker1}: {df1.columns}")
    print(f"Flattened Columns for {ticker2}: {df2.columns}")

    # Merge the two dataframes on the 'Date' index
    merged_df = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=(f'_{ticker1}', f'_{ticker2}'))

    # Reset index to flatten the index
    merged_df = merged_df.reset_index()

    # Ensure column names are correct (strip any leading/trailing spaces)
    merged_df.columns = merged_df.columns.str.strip()

    # Check if all required columns are present
    required_columns = {
        f'{ticker1}_Open', f'{ticker1}_High', f'{ticker1}_Low', f'{ticker1}_Close', f'{ticker1}_Adj Close',
        f'{ticker2}_Open', f'{ticker2}_High', f'{ticker2}_Low', f'{ticker2}_Close', f'{ticker2}_Adj Close'
    }

    # Check if all required columns are present in the merged dataframe
    missing_columns = required_columns - set(merged_df.columns)
    if missing_columns:
        print(f"Columns missing: {missing_columns}")
        raise ValueError(f"Data is missing required columns: {missing_columns}.")

    return merged_df



def plot_data(data, indicators, sync_axis=None):
    if data.empty:
        raise ValueError("No data available for plotting.")

    # Ensure the data has the required columns
    required_columns = {'Open', 'Close', 'High', 'Low'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Data is missing required columns: {required_columns - set(data.columns)}")

    gain = (data['Close'] > data['Open']).values  # Convert to 1D boolean array
    loss = (data['Open'] > data['Close']).values  # Convert to 1D boolean array
    width = 12 * 60 * 60 * 1000  # Width for candlesticks in milliseconds

    # Create Bokeh figure
    if sync_axis is not None:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000, x_range=sync_axis)
    else:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1000)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.25

    # Add candlestick chart
    p.segment(data.index, data['High'], data.index, data['Low'], color="black")
    p.vbar(data.index[gain], width, data['Open'][gain].values, data['Close'][gain].values, fill_color="#00ff00", line_color="#00ff00")
    p.vbar(data.index[loss], width, data['Open'][loss].values, data['Close'][loss].values, fill_color="#ff0000", line_color="#ff0000")

    # Add selected indicators
    for indicator in indicators:
        if indicator == "30 Day SMA":
            data['SMA30'] = data['Close'].rolling(window=30).mean()
            p.line(data.index, data['SMA30'], color="purple", legend_label="30 Day SMA")

        elif indicator == "100 Day SMA":
            data['SMA100'] = data['Close'].rolling(window=100).mean()
            p.line(data.index, data['SMA100'], color="orange", legend_label="100 Day SMA")

        elif indicator == "Linear Regression Line":
            x_vals = np.arange(len(data.index))
            y_vals = data['Close'].values
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            y_predicted = slope * x_vals + intercept
            p.line(data.index, y_predicted, legend_label="Linear Regression", color="red")

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    return p

def on_button_click(ticker1, ticker2, start, end, indicators):
    try:
        df1, df2 = load_data(ticker1, ticker2, start, end)
        p1 = plot_data(df1, indicators)
        p2 = plot_data(df2, indicators, sync_axis=p1.x_range)
        curdoc().clear()
        curdoc().add_root(layout)
        curdoc().add_root(row(p1, p2))
    except Exception as e:
        print(f"Error: {e}")

# Bokeh Widgets
stock1_text = TextInput(title="Stock 1")
stock2_text = TextInput(title="Stock 2")
date_picker_from = DatePicker(title="Start Date", value="2024-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title="End Date", value="2024-02-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
indicator_choice = MultiChoice(options=["100 Day SMA", "30 Day SMA", "Linear Regression Line"])

# Load button setup
load_button = Button(label="Load Data", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, indicator_choice.value))

# Layout
layout = column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button)
curdoc().clear()
curdoc().add_root(layout)
