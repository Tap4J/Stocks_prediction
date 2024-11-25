import numpy as np
import math
import pandas as pd
import yfinance as yf
import datetime as dt

from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import TextInput, Button, DatePicker, Toggle, ColumnDataSource, DataTable, TableColumn, StringFormatter, CheckboxGroup

def load_data(ticker1, ticker2, start, end):
    df1 = yf.download(ticker1, start=start, end=end)
    df2 = yf.download(ticker2, start=start, end=end)

    #I need to rename columns (multindex)
    df1 = df1.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    df2 = df2.rename(columns={'Adj Close': 'Adj Close', 'Close': 'Close', 'High': 'High', 'Low': 'Low', 'Open': 'Open', 'Volume': 'Volume'})
    
    return df1, df2

def update_plot(data, ticker, indicators, show_legend, sync_axis=None):
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
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1200, x_range=sync_axis, title=ticker)
    else:
        p = figure(x_axis_type="datetime", tools="pan,wheel_zoom,box_zoom,reset,save", width=1200, title=ticker)

    p.xaxis.major_label_orientation = math.pi / 4
    p.grid.grid_line_alpha = 0.5
    p.title.align = "center"
    p.title.text_font_size = "20pt"
    p.title.text_font_style = "bold" 

    legend_high_low = "High-Low" if show_legend else ""
    legend_gain = "Gain" if show_legend else ""
    legend_loss = "Loss" if show_legend else ""
    legend_30 = "30 Day SMA" if show_legend else ""
    legend_100 = "100 Day SMA" if show_legend else ""
    legend_lr = "Linear Regression" if show_legend else ""


    # Plot the data
    p.segment(data.index, data[high_col], data.index, data[low_col], color="black", legend_label=legend_high_low)
    p.vbar(data.index[gain], width, data[open_col][gain], data[close_col][gain], fill_color="#00ff00", line_color="#00ff00", legend_label=legend_gain)
    p.vbar(data.index[loss], width, data[open_col][loss], data[close_col][loss], fill_color="#ff0000", line_color="#ff0000", legend_label=legend_loss)
    
    # Definition for indicators
    for indicator in indicators:
        print(indicator)
        if indicator== "30 Day SMA":
            data['SMA30'] = data[close_col].rolling(30).mean()
            p.line(data.index, data['SMA30'], color="purple", legend_label=legend_30)

        elif indicator== "100 Day SMA":
            data['SMA100'] = data[close_col].rolling(100).mean()
            p.line(data.index, data['SMA100'], color="orange", legend_label=legend_100)


        elif indicator== "Linear Regression Line":
            x_vals = np.arange(len(data.index))
            y_vals = data['Close'].values
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            y_predicted = slope * x_vals + intercept
            p.line(data.index, y_predicted, legend_label=legend_lr, color="red")

    if show_legend:
        p.legend.location = "top_left"
        p.legend.click_policy = "hide"
    else:
        p.legend.visible = False

    return p


def on_button_click(main_stock, comparison_stock, start, end, legend_checkbox):
    try:
        selected_indicators = []
        if toggle_100.active:
            selected_indicators.append("100 Day SMA")
        if toggle_30.active:
            selected_indicators.append("30 Day SMA")
        if toggle_lr.active:
            selected_indicators.append("Linear Regression Line")
        
        show_legend = 0 in legend_checkbox.active

        # Loading data for first ticker and second ticker, adding dates
        df1, df2 = load_data(main_stock, comparison_stock, start, end)
        if df1.empty or df2.empty:
            print("One or both data sources are empty. Check stock tickers and date range.")
            return
        
        # Call function for plot
        p = update_plot(df1, main_stock, selected_indicators, show_legend=show_legend)
        p2 = update_plot(df2, comparison_stock, selected_indicators, show_legend=show_legend)

        updated_layout = column(layout, row(p, p2))
        curdoc().clear()
        curdoc().add_root(updated_layout)
    except Exception as e:
       print(f"Error: {e}")

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

stock1_text = TextInput(title="Main Stock", value='TSLA')
stock2_text = TextInput(title="Comparison Stock", value='AAPL')
date_picker_from = DatePicker(title='Start Date', value="2024-01-01", min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
date_picker_to = DatePicker(title='End Date', value=dt.datetime.now().strftime("%Y-%m-%d"), min_date="2000-01-01", max_date=dt.datetime.now().strftime("%Y-%m-%d"))
toggle_100 = Toggle(label="100 Day SMA", active=False)
toggle_30 = Toggle(label="30 Day SMA", active=False)
toggle_lr = Toggle(label="Linear Regression Line", active=False)
legend_checkbox  = CheckboxGroup(labels=["Show legend"], active=[0])

indicator_choice = column(toggle_100, toggle_30, toggle_lr, legend_checkbox)

load_button = Button(label="Apply", button_type="success")
load_button.on_click(lambda: on_button_click(stock1_text.value, stock2_text.value, date_picker_from.value, date_picker_to.value, legend_checkbox))

layout = row(
    column(stock1_text, stock2_text, date_picker_from, date_picker_to, indicator_choice, load_button),
    ticker_table
)

curdoc().clear()
curdoc().add_root(layout)