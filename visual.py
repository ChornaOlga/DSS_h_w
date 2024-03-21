import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from yahoo_parse import *
from prediction import *


def model_visualise(data, model, text=''):
    """
        Visualize the original model and the model estimated using the method of least squares (MNK).

        Parameters:
        - model (array-like): Input array representing the original model.
        - text (str): Additional text for the y-axis label.

        Returns:
        None
    """
    N_DAYS_AGO = 99
    pred_length = 7

    today = datetime.now()
    date_range = pd.date_range((today - timedelta(days=N_DAYS_AGO)).date(),
                               (today + timedelta(days=pred_length)).date(),
                               freq='D')

    a = np.full(pred_length, np.nan)
    data = np.append(data, a)

    data_dict = {'date': date_range, 'real_value': data, 'prediction': model}
    df = pd.DataFrame(data_dict)
    df = df.set_index('date')

    fig = plt.subplots(figsize=(16, 5))
    plt.plot(df.index, df['real_value'], label='Reality')
    plt.plot(df.index, df['prediction'], label='Expectation')
    plt.title('USD for '+text+' rate', fontsize=20)
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('Rate', fontsize=15)
    plt.xlim(df.index.min(), df.index.max())

    # Display the plot
    plt.show()


if __name__ == "__main__":
    url = 'https://finance.yahoo.com/quote/BTC-USD/history/'
    data = bs4_url_to_pandas(url, 'Open')
    model_visualise(data, regr_pred(data), text=url)