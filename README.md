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
**Run Jupyter Lab with the Notebook and Data**

To run the Jupyter Notebook with all the data in the GitHub repository, follow these steps:

1. Ensure you are still in the project directory.
2. Start Jupyter Lab:

    ```sh
    jupyter lab
    ```
3. A new tab will open in your default web browser, displaying the Jupyter Lab interface.
4. In Jupyter Lab, navigate to the directory where the notebook file (`.ipynb`) is located.
5. Open the notebook file to begin working with it.


## Dashboard

Simple dashboard to visualize data for 2 companies (Tickers -> shortcut for company)   (TBD List of popular tickers!)

1. Select Ticker from the list and input (example values already added)
2. Select dates (example values already added)
3. Select from multichoice indicator (multiple-choice) // TBD fixing 100SMA
4. Load data
5. Play with dashboard!

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
