import pandas as pd

dict_to_df = {'country_name': ['Canada',
                               'Brazil',
                               'Switzerland',
                               'United Kingdom',
                               'Japan',
                               'India',
                               'South Africa',
                               'Turkiye',
                               'Mexico',
                               'Poland',
                               'Germany'
                               ],

              'country_name_abbv': ['CAN',
                                    'BRA',
                                    'SWZ',
                                    'UKD',
                                    'JPN',
                                    'IND',
                                    'SAF',
                                    'TKY',
                                    'MEX',
                                    'POL',
                                    'GER'
                                    ],

              'country_currency': ['CAD',
                                   'BRL',
                                   'CHF',
                                   'GBP',
                                   'JPY',
                                   'INR',
                                   'ZAR',
                                   'TRY',
                                   'MXN',
                                   'PLN',
                                   'EUR']

              }

criteria = {'criteria_name': ['power_index',
                              'currency_value_in_usd',
                              'delta_percent',
                              'recommendation',
                              'buy',
                              'neutr',
                              'sell',
                              'happiness_score',
                              'economy_score',
                              'human_development_index_growth',
                              'IMF_Forecast_GDP',
                              'World_Bank_Forecast_GDP',
                              'CIA_Forecast_GDP',
                              'population_growth'
                              ],
            'optimize': ['min',
                         'max',
                         'max',
                         'max',
                         'max',
                         'min',
                         'min',
                         'max',
                         'max',
                         'max',
                         'max',
                         'max',
                         'max',
                         'max'
                         ]
            }

if __name__ == '__main__':
    countries_df = pd.DataFrame.from_dict(dict_to_df)
    print(countries_df)
