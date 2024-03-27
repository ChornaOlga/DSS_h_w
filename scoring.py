# ----------------------------- Optimization: scoring models + OLAP ------------------------------------

"""
    Завдання:
       сформувати обгрунтоване рішення щодо вибору валюти для інвестування.
       Кліент має у розпорядженні деяку сумму у USD,
       необхідно оцінити певну кількість валют інших країн та обрати найкращій варіант для інвестування.

    Склад етапів:
    1. Формалізація задачі як багатофакторної / багатокритеріальної:
        По результатм краткого дослідження предметної області було обрано 14 факторів які можуть бути враховані
        для обрання стабільної та актуальної валюти.
    2. Формування сегменту даних та парсінг *.xls файлу:
        В якості даних використано:
        2.1 Парсинг актуального стану відповідних валют з сайта присвяченого інвестиціям
        2.2 Парсинг .csv файлів з інформацією про економічне та соціальне ранжування відповідних країн
        Результатом збору даних є файл matrix_for_score.csv. Rows description:
        power_index: the country's 2023 power score (lower number is stronger militarily)
        currency_value_in_usd: latest cross course usd/currency
        delta_percent: latest delta in currency conversion rate (percentage)
        recommendation: recommendation from investment url in order from 1 to 5,
                        where 1 - mean you need to actively sell this investment,
                        5 - mean you need to actively buy this investment
        buy: number of technical indicators in favor of buying this investment
        neutr: number of technical indicators in favor of doing nothing with this investment
        sell: number of technical indicators in favor of selling this investment
        happiness_score: score based on six factors – economic production, social support, life expectancy,
                                                        freedom, absence of corruption, and generosity
        economy_score: 2023 Index of Economic Freedom, based on: Property Rights, Judicial Effectiveness,
                                                                 Government Integrity, Tax Burden, Business Freedom,
                                                                 Investment Freedom, etc.

        human_development_index_growth: Percentage growth in Human Development Index, a measure of a country's overall
                                        achievement in its social and economic dimensions.
        IMF_Forecast_GDP: IMF's forecast for Gross Domestic Product in purchasing power parity terms.
        World_Bank_Forecast_GDP: World Bank's forecast for Gross Domestic Product in purchasing power parity terms.
        CIA_Forecast_GDP: Central Intelligence Agency's forecast for Gross Domestic Product in purchasing power parity terms.
        population_growth: Percentage change in population from 2022 to 2023.

    3. Нормалізація даних:
        нормалізація даних проведена двома способами.
        1. У методі Voronin - вручну
        2. У методі Voronin_sklearn - за допомогою scaler-а типу Normalizer() з бібліотеки sklearn

    4. Розрахунок інтегрованої оцінки - scor - оцінювання альтернатив - scoring;
       спосіб розрашунку інтегрованої оцінки - нелінійна схема компромісів
       http://sci-gems.math.bas.bg/jspui/bitstream/10525/49/1/ijita15-2-p02.pdf

    5. Обрання найкращіх альтернатив.

    6. OLAP - візуалізація методами Matplotlib - змінена за разунок використання тривимірної bar діаграми
    https://matplotlib.org/stable/api/_as_gen/mpl_toolkits.mplot3d.axes3d.Axes3D.bar3d.html

"""

import numpy as np

from countries_data_combine import create_country_scoring_matrix
from voronin import Voronin, Voronin_sklearn


def scoring():
    """
        Calculate scores for alternatives based on a scoring matrix and recommend currencies for long-term investments.

        This function reads a scoring matrix from a CSV file, calculates scores using the Voronin method with given preference coefficients,
        and recommends currencies for long-term investments based on the calculated scores.

        Returns:
        - None
    """
    File_name = 'data/matrix_for_score.csv'
    create_country_scoring_matrix(File_name)

    # ---------------- коефіціенти переваги критеріїв -----------------
    criteria_preference_coefficients_list = np.ones(14)

    scores_df = Voronin(File_name, criteria_preference_coefficients_list)
    print('All alternatives and their scores are next:')
    print(scores_df)
    print('Based on information above we recommend you to consider'
          ' the following currency(ies) for long term investments:')
    print(scores_df[scores_df['if_best']])
    print('And now is appropriate time to buy such assets!')


if __name__ == '__main__':
    scoring()
