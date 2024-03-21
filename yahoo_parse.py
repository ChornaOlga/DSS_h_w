import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup

def bs4_url_to_pandas(url, Data_name):
    """
            Parse HTML tables from a yahoo URL using beautiful soup and extract a specific column of numerical data.

            Parameters:
            - url (str): The URL of the webpage containing HTML tables to parse.
            - Data_name (str): The name of the column whose numerical data needs to be extracted.

            Returns:
            - numpy.ndarray: A NumPy array containing the numerical data from the specified column.
            """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', attrs={'class': 'W(100%) M(0)'})
    table_rows = table.find_all('tr')
    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all('td'):
            row_data.append(cell.text.replace(',', ''))
        data.append(row_data)
    df = pd.DataFrame(data)
    df.drop(df.tail(1).index, inplace=True)
    df.drop(df.head(1).index, inplace=True)
    df.columns = ['Date', 'Open', 'High', 'Low', 'Close*', 'Adj Close**', 'Volume']
    df = df[::-1]
    pd.set_option('future.no_silent_downcasting', True)
    df.replace('-', np.nan, inplace=True)
    df[Data_name] = df[Data_name].astype(float)
    model_real = df[Data_name].to_numpy()
    print('Джерело даних: ', url)
    return model_real


if __name__ == '__main__':
    url = 'https://finance.yahoo.com/quote/BTC-USD/history/'
    # Model = parser_url_to_pandas(url, 'Open')
    Model = bs4_url_to_pandas(url, 'Open')
    print(Model)