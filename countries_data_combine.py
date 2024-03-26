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
                                  class_=re.compile(
                                      'mb-6 mt-1 rounded-full px-4 py-1.5 text-center -mt-2.5 font-semibold leading-5 text-white')).get_text()
        asset_list.append(convert(recomendation))
        badges = soup.body.find('div', {'class': 'flex items-center gap-x-4 text-xs md2:gap-x-3.5 lg:gap-x-4'})
        for span in badges.find_all('span', class_=re.compile('font-bold')):
            indicators_number = span.get_text()
            asset_list.append(str_to_float(indicators_number))

    return asset_list


def extract_mil_df():
    mil_df = pd.read_csv('data/military/military_data_2023.csv')
    mil_df = mil_df[['country_name_abbv', 'power_index']]

    return mil_df


def extract_happiness_df():
    happy_df = pd.read_csv('data/happiness/world_happiness_rank_2023.csv')
    happy_df.rename(columns={'Country name': 'country_name', 'Ladder score': 'happiness_score'}, inplace=True)
    happy_df = happy_df[['country_name', 'happiness_score']]

    return happy_df


def extract_economy_df():
    economy_df = pd.read_csv('data/economy/world_economy_freedom.csv')
    economy_df.rename(columns={'Country Name': 'country_name', '2023 Score': 'economy_score'}, inplace=True)
    economy_df = economy_df[['country_name', 'economy_score']]

    economy_df.replace(to_replace='Turkey',
                       value='Turkiye', inplace=True)

    return economy_df


def extract_wiki_stat_df():
    wiki_stat_df = pd.read_csv('data/wikipedia_statistics/Country_data.csv')

    wiki_stat_df.rename(columns={'Country': 'country_name',
                                 '%HDI Growth': 'human_development_index_growth',
                                 'IMF Forecast GDP(PPP)': 'IMF_Forecast_GDP',
                                 'World Bank Forecast GDP(PPP)': 'World_Bank_Forecast_GDP',
                                 'CIA Forecast GDP(PPP)': 'CIA_Forecast_GDP',
                                 'Population %Change': 'population_growth'}, inplace=True)

    wiki_stat_df = wiki_stat_df[['country_name',
                                 'human_development_index_growth',
                                 'IMF_Forecast_GDP',
                                 'World_Bank_Forecast_GDP',
                                 'CIA_Forecast_GDP',
                                 'population_growth']]

    # economy_df.replace(to_replace='Turkey',
    #                    value='Turkiye', inplace=True)

    return wiki_stat_df


def extract_invest_df():
    df = pd.read_csv('data/investing_froze_25_03_2024.csv')

    # #get countries data
    # countries_df = pd.DataFrame.from_dict(dict_to_df)
    # currency_id = countries_df['country_currency'].to_list()
    #
    # df_values = []
    #
    # #parse hot data from url
    # for currency in currency_id:
    #     url = 'https://ru.investing.com/currencies/' + currency.lower() + '-usd-technical'
    #     a_list = url_parse(url)
    #     a_list.insert(0, currency)
    #     df_values.append(a_list)
    #
    # #combine data in dataframe
    # df = pd.DataFrame(df_values, columns=['country_currency',
    #                                       'currency_value_in_usd',
    #                                       'delta_percent',
    #                                       'recommendation',
    #                                       'buy',
    #                                       'neutr',
    #                                       'sell'
    #                                       ]
    #                   )

    return df


def expand_df(df_to_expand, func, on_column):
    df_to_add = func()
    expanded_df = df_to_expand.join(df_to_add.set_index(on_column), on=on_column)
    return expanded_df


def create_country_scoring_matrix(file_to_write):
    # create initial dataframe
    countries_df = pd.DataFrame.from_dict(dict_to_df)

    # dataframe expantion
    combine_df = expand_df(countries_df, extract_mil_df, on_column='country_name_abbv')
    combine_df = expand_df(combine_df, extract_invest_df, on_column='country_currency')
    combine_df = expand_df(combine_df, extract_happiness_df, on_column='country_name')
    combine_df = expand_df(combine_df, extract_economy_df, on_column='country_name')
    combine_df = expand_df(combine_df, extract_wiki_stat_df, on_column='country_name')

    # dataframe crop, resize and transpond
    combine_df.drop(['country_name', 'country_currency'], axis=1, inplace=True)
    combine_df.set_index('country_name_abbv')
    combine_df_transposed = combine_df.T
    combine_df_transposed.rename(columns=combine_df_transposed.iloc[0], inplace=True)
    combine_df_transposed.drop(combine_df_transposed.index[0], inplace=True)

    # dataframe export to file
    combine_df_transposed.to_csv(file_to_write)


if __name__ == '__main__':
    path_to_write_matrix = 'data/result.csv'
    create_country_scoring_matrix(path_to_write_matrix)
