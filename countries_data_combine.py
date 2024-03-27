import numpy as np
import pandas as pd
import requests
import re

from bs4 import BeautifulSoup

from glossary import *


def str_to_float(str):
    """
        Convert a string representation of a percentage to a float.

        This function removes any parentheses and commas from the input string,
        replaces the decimal delimiter if needed, and converts the resulting string to a float.

        Parameters:
        - str (str): The string representation of a percentage.

        Returns:
        - float: The converted float value.
    """
    return float(str.strip('(%)').replace('.', '').replace(',', '.'))


def convert(sell_key):
    """
        Convert a textual representation of selling sentiment to a numerical value.

        This function takes a string representing the selling sentiment and returns a numerical value based on a predefined dictionary.

        Parameters:
        - sell_key (str): The textual representation of selling sentiment.

        Returns:
        - float: The numerical value corresponding to the selling sentiment.

        Raises:
        - KeyError: If the sell_key is not found in the sell_dict.
    """
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
        Scrape financial data from a given URL and parse specific values.

        This function fetches the webpage content from the provided URL, extracts financial data,
        and returns a list containing the parsed values.

        Parameters:
        - url (str): The URL of the webpage containing the financial data.

        Returns:
        - list: A list containing the parsed financial data values.
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
    """
        Extract military data from a CSV file for the year 2023.

        This function reads a CSV file containing military data for the year 2023,
        extracts specific columns ('country_name_abbv' and 'power_index'),
        and returns a DataFrame containing this extracted data.

        Returns:
        - pandas.DataFrame: A DataFrame containing the extracted military data.
    """
    mil_df = pd.read_csv('data/military/military_data_2023.csv')
    mil_df = mil_df[['country_name_abbv', 'power_index']]

    return mil_df


def extract_happiness_df():
    """
        Extract world happiness rank data from a CSV file for the year 2023.

        This function reads a CSV file containing world happiness rank data for the year 2023,
        renames specific columns ('Country name' to 'country_name' and 'Ladder score' to 'happiness_score'),
        and returns a DataFrame containing this extracted and renamed data.

        Returns:
        - pandas.DataFrame: A DataFrame containing the extracted world happiness rank data.
    """
    happy_df = pd.read_csv('data/happiness/world_happiness_rank_2023.csv')
    happy_df.rename(columns={'Country name': 'country_name', 'Ladder score': 'happiness_score'}, inplace=True)
    happy_df = happy_df[['country_name', 'happiness_score']]

    return happy_df


def extract_economy_df():
    """
        Extract world economy freedom data from a CSV file.

        This function reads a CSV file containing world economy freedom data,
        renames specific columns ('Country Name' to 'country_name' and '2023 Score' to 'economy_score'),
        replaces a specific country name ('Turkey' with 'Turkiye'),
        and returns a DataFrame containing this extracted, renamed, and modified data.

        Returns:
        - pandas.DataFrame: A DataFrame containing the extracted world economy freedom data.
    """
    economy_df = pd.read_csv('data/economy/world_economy_freedom.csv')
    economy_df.rename(columns={'Country Name': 'country_name', '2023 Score': 'economy_score'}, inplace=True)
    economy_df = economy_df[['country_name', 'economy_score']]

    economy_df.replace(to_replace='Turkey',
                       value='Turkiye', inplace=True)

    return economy_df


def extract_wiki_stat_df():
    """
        Extract country statistics from a Wikipedia statistics CSV file.

        This function reads a CSV file containing country statistics from Wikipedia,
        renames specific columns to more readable names,
        replaces a specific country name ('Turkey' with 'Turkiye'),
        and returns a DataFrame containing this extracted, renamed, and modified data.

        Returns:
        - pandas.DataFrame: A DataFrame containing the extracted country statistics.
    """
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

    wiki_stat_df.replace(to_replace='Turkey',
                       value='Turkiye', inplace=True)

    return wiki_stat_df


def extract_invest_df():
    """
        Extract investment data related to various countries' currencies from a website.

        This function extracts investment data related to various countries by parsing a URL for each country's currency.
        The parsed data includes currency value in USD, delta percent, recommendations, buy, neutral, and sell values.
        The extracted data is combined into a DataFrame and returned.

        Returns:
        - pandas.DataFrame: A DataFrame containing the extracted investment data.
    """
    #get countries data
    countries_df = pd.DataFrame.from_dict(dict_to_df)
    currency_id = countries_df['country_currency'].to_list()

    df_values = []

    #parse hot data from url
    for currency in currency_id:
        url = 'https://ru.investing.com/currencies/' + currency.lower() + '-usd-technical'
        a_list = url_parse(url)
        a_list.insert(0, currency)
        df_values.append(a_list)

    #combine data in dataframe
    df = pd.DataFrame(df_values, columns=['country_currency',
                                          'currency_value_in_usd',
                                          'delta_percent',
                                          'recommendation',
                                          'buy',
                                          'neutr',
                                          'sell'
                                          ]
                      )

    return df


def expand_df(df_to_expand, func, on_column):
    """
        Expand a given DataFrame by joining it with another DataFrame returned by a specified function.

        This function expands a given DataFrame `df_to_expand` by joining it with another DataFrame
        returned by a specified function `func`. The join is performed based on a specified column `on_column`.

        Parameters:
        - df_to_expand (pandas.DataFrame): The DataFrame to expand.
        - func (function): A function that returns a DataFrame to join with `df_to_expand`.
        - on_column (str): The column name based on which the join operation should be performed.

        Returns:
        - pandas.DataFrame: An expanded DataFrame containing the original columns of `df_to_expand`
          and the additional columns from the DataFrame returned by `func`.
    """
    df_to_add = func()
    expanded_df = df_to_expand.join(df_to_add.set_index(on_column), on=on_column)
    return expanded_df


def create_country_scoring_matrix(file_to_write):
    """
        Create a scoring matrix for countries currencies based on various data sources.

        This function creates a scoring matrix for countries currencies by expanding a base DataFrame with
        additional data related to military power, investment, happiness, economy, and Wikipedia
        statistics. The expanded DataFrame is transposed and exported to a specified file.

        Parameters:
        - file_to_write (str): The path to the file where the scoring matrix should be saved.

        Returns:
        - None: The function does not return anything, but saves the scoring matrix to a file.
    """
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
    path_to_write_matrix = 'data/matrix_for_score.csv'
    create_country_scoring_matrix(path_to_write_matrix)
