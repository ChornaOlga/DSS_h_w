import numpy as np
import pandas as pd
import requests
import re

from bs4 import BeautifulSoup

from glossary import *


def str_to_float(str):
    return float(str.strip('(%)').replace('.', '').replace(',', '.'))


def convert(sell_key):
    sell_dict = {
        'Активно продавать': 1.,
        'Продавать': 2.,
        'Нейтрально': 3.,
        'Покупать': 4.,
        'Активно покупать': 5.
    }
    return sell_dict[sell_key]


def url_parse(url):
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
    asset_list = []

    current_value = None
    while current_value is None:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        current_value = soup.find('div', attrs={'data-test': 'instrument-price-last'}).get_text()
        asset_list.append(str_to_float(current_value))
        price_change = soup.find('span', attrs={'data-test': 'instrument-price-change-percent'}).get_text()
        asset_list.append(str_to_float(price_change))
        recomendation = soup.find('div',
                                  class_=re.compile('mb-6 mt-1 rounded-full px-4 py-1.5 text-center -mt-2.5 font-semibold leading-5 text-white')).get_text()
        asset_list.append(convert(recomendation))
        badges = soup.body.find('div', {'class': 'flex items-center gap-x-4 text-xs md2:gap-x-3.5 lg:gap-x-4'})
        for span in badges.find_all('span', class_=re.compile('font-bold')):
            indicators_number = span.get_text()
            asset_list.append(str_to_float(indicators_number))

    return asset_list

def extract_mil_df():
    mil_df = pd.read_csv('data/military_data_2023.csv')
    countries_list = [item for sublist in list(countries_dict.values()) for item in sublist]
    mil_df = mil_df[mil_df['country_name'].isin(countries_list)].reset_index(drop=True)

    return mil_df


def extract_invest_df():
    df_values = []
    for key, value in currencies_cross_course_dictionary.items():
        url = 'https://ru.investing.com/currencies/' + value
        a_list = url_parse(url)
        a_list.insert(0, key)
        a_list.insert(1, countries_dict[key.split('/')[0]][1])
        df_values.append(a_list)
    df = pd.DataFrame(df_values, columns=['currency_key', 'country_name_abbv', 'value', 'delta_perc', 'recommendation', 'buy', 'neutr', 'sell'])

    return df


if __name__ == '__main__':
    milit_df = extract_mil_df()
    investment_rec_df = extract_invest_df()
    milit_df = milit_df.join(investment_rec_df, lsuffix='_left')
    # print(milit_df)
    # milit_df.to_csv('res.csv')
