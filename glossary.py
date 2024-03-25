import pandas as pd

yahoo_watchlist_dictionary = {'канадський долар': 'CADUSD%3DX',
                              'австралійський долар': 'AUDUSD%3DX',
                              'швейцарський франк': 'CHFUSD%3DX',
                              'євро': 'EURUSD%3DX',
                              'фунт стерлінгів': 'GBPUSD%3DX',
                              'японська єна': 'JPYUSD%3DX',
                              'новозеландський долар': 'NZDUSD%3DX',
                              'південноафриканський ранд': 'ZARUSD%3DX',
                              'турецька ліра': 'TRYUSD%3DX',
                              'мексиканский песо': 'MXNUSD%3DX',
                              'злотий': 'PLNUSD%3DX',
                              'десятирічна облігація сша': '%5ETNX',
                              'нафта crude': 'CL%3DF',
                              'золото': 'GC%3DF',
                              'срібло': 'SI%3DF',
                              'bitcoin': 'BTC-USD'
                              }

currencies_cross_course_dictionary = {'CAD/USD': 'cad-usd-technical',
                                      'AUD/USD': 'aud-usd-technical',
                                      'CHF/USD': 'chf-usd-technical',
                                      'GBP/USD': 'gbp-usd-technical',
                                      'JPY/USD': 'jpy-usd-technical',
                                      'NZD/USD': 'nzd-usd-technical',
                                      'ZAR/USD': 'zar-usd-technical',
                                      'TRY/USD': 'try-usd-technical',
                                      'MXN/USD': 'mxn-usd-technical',
                                      'PLN/USD': 'pln-usd-technical'
                                      }

dict_to_df = {'country_name': ['Canada',
                               'Australia',
                               'Switzerland',
                               'United Kingdom',
                               'Japan',
                               'New Zealand',
                               'South Africa',
                               'Turkiye',
                               'Mexico',
                               'Poland'],

              'country_name_abbv': ['CAN',
                                    'AUS',
                                    'SWZ',
                                    'UKD',
                                    'JPN',
                                    'NWZ',
                                    'SAF',
                                    'TKY',
                                    'MEX',
                                    'POL'],

              'country_currency': ['CAD',
                                   'AUD',
                                   'CHF',
                                   'GBP',
                                   'JPY',
                                   'NZD',
                                   'ZAR',
                                   'TRY',
                                   'MXN',
                                   'PLN']

              }

criteria = {'criteria_name': ['power_index',
                              'value',
                              'delta_perc',
                              'recommendation',
                              'buy',
                              'neutr',
                              'sell',
                              'happiness_score',
                              'economy_score'],
            'optimize': ['min',
                         'max',
                         'max',
                         'max',
                         'max',
                         'min',
                         'min',
                         'max',
                         'max'
                         ]
            }

if __name__ == '__main__':
    countries_df = pd.DataFrame.from_dict(dict_to_df)
    print(countries_df)
