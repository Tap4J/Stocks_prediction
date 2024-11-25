# Stock prediction using Bokeh + yfinance API + Keras
Dashboard + stock prediction for financial data

## Guidelines
**Install Libraries from Requirements Using pip**
1. Open your terminal (macOS/Linux) or command prompt (Windows).
2. Navigate to the directory where you have downloaded/cloned the repository.
    ```sh
    cd path/to/your/project
    ```
3. (Optional) Create and activate a virtual environment:
      ```sh
      python3 -m venv env
      source venv/bin/activate
      ```
5. Install the required libraries using `pip`: (THIS STEP TBD SOON!)

    ```sh
    pip install -r requirements.txt
    ```
**Run Python file with prediction**

To run the Python file follow these steps:

1. Ensure you are in the project directory running a virtual environment with installed libraries.
2. Open your command prompt and type:

    ```sh
    python stock_prediction.py
    ```
3. After your program finishes training, a new pop will open with predicted data for "Meta"
4. If you wish to change the company, open file in your project directory and change the variables "company, start, end"
5. Adjust other attributes if you wish to

**Run Dashboard**

To run the Dashboard follow these steps:

1. Ensure you are in the project directory running a virtual environment with installed libraries.
2. Open your command prompt and type:

    ```sh
    bokeh serve --show dashboard.py
    ```
3. This will automatically open a new browser window with a running dashboard

## Dashboard

Simple dashboard to visualize data for 2 companies (Tickers -> shortcut for company)

1. Select Ticker from the list of "Available tickers" and input them into field (example values already added)
2. Select dates (example values already added)
3. Toggle indicator (multiple-choice)
    - 30 day average of the closing price
    - 100 day average of the closing price
    - Linear Regression Line
5. Select checkbox to show legend
6. Apply changes by clicking on "Apply"
7. Play with dashboard!
![image](https://github.com/user-attachments/assets/b1cd63f3-89bc-4920-8b6a-6e2a20ecb3c4)


## Stock prediction

1. **Data preparation**
    - Scaling data with MinMaxScaler and reshape
    - Train, test split and train on data except prediction days (later on conduct testing)
2. **Define Model**
    - Define model units
    - Fit model and select unit of epochs
3. **Test the model**
    - Download data from yfinance 
    - Define and adjust for model inputs
4. **Make prediction**
    - Make prediction on testing data (Predict the selected amount of prediction days and compare)
    - Plot test prediction
    - Predict next days data (prediction on new data)
    - Example:
![image](https://github.com/user-attachments/assets/5e0e972c-a836-4a78-be0a-eab7cd351eec)

