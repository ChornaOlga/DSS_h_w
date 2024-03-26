# ----------------------------- Optimization: scoring models + OLAP ------------------------------------

'''

Завдання:
   сформувати обгрунтоване рішення щодо впровадження нового товару на ринок з множини альтернатив

Склад етапів:
1. Формалізація задачі як багатофакторної / багатокритеріальної;
2. Формування сегменту даних та парсінг *.xls файлу;
3. Нормалізація даних;
4. Розрахунок інтегрованої оцінки - scor - оцінювання альтернатив - scoring;
   спосіб розрашунку інтегрованої оцінки - нелінійна схема компромісів
   http://sci-gems.math.bas.bg/jspui/bitstream/10525/49/1/ijita15-2-p02.pdf
5. Обрання найкращіх альтернатив.
6. OLAP - візуалізація методами Matplotlib - PyLab module https://matplotlib.org/stable/gallery/mplot3d/index.html

Альтернативні галузі:
   Теорія операцій - розподіл ресурсів;
   Теорія розкладів
   Інструментарій оптимізації: Google OR-Tools;
   https://developers.google.com/optimization/examples?hl=en

Алтернативні бібліотеки для OLAP:
https://olapy.readthedocs.io/en/latest/
https://pythonhosted.org/cubes/

Package                      Version
---------------------------- -----------
pip                          23.1
pandas                       1.5.3
numpy                        1.23.5
matplotlib                   3.6.2

'''

# import sys
import pandas as pd
import numpy as np
import pylab
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from glossary import criteria


def matrix_generation(File_name):
    sample_data_df = pd.read_csv(File_name)
    sample_data_df.drop(columns=sample_data_df.columns[0], axis=1, inplace=True)
    line_column_matrix = sample_data_df.to_numpy()

    return line_column_matrix

def alternatives_names(File_name):
    sample_data_df = pd.read_csv(File_name)
    header = list(sample_data_df.columns)
    header.pop(0)
    return header


def Voronin(File_name, criteria_coef):
    # --------------------- вхідні дані -------------------------
    line_column_matrix = matrix_generation(File_name)
    features_number = np.shape(line_column_matrix)[0]
    alternatives_number = np.shape(line_column_matrix)[1]
    alternatives = alternatives_names(File_name)

    # --------------- нормалізація вхідних даних ------------------
    # copying features for normalization
    features_norm = np.copy(line_column_matrix)

    # criteria coefficients normalization
    criteria_coef_norm = criteria_coef / criteria_coef.sum()

    # changing features->max to the 1/feature
    for index, opt_direction in enumerate(criteria['optimize']):
        if opt_direction == 'max':
            features_norm[index] = 1 / features_norm[index]

    # features normalization
    features_norm_sum = features_norm.sum(axis=1)
    features_norm = np.divide(features_norm.T, features_norm_sum).T

    print(features_norm)

    # calculating integrated score in few steps
    integro_1 = features_norm.T
    integro_2 = (1 - integro_1)
    integro_3 = np.power(integro_2, (-1))
    integro_4 = integro_3 * criteria_coef_norm
    integro_5 = integro_4.sum(axis=1)

    # print(integro_5)

    result_dict = {'currency': alternatives,
                 'score': integro_5,
                 'if_best': integro_5 == np.min(integro_5, axis=0)}

    # --------------- генерація оптимального рішення ----------------
    result_df = pd.DataFrame(result_dict)

    Data_mode = input('Do you want an OLAP cube of your alternatives? (y/n)\n')

    if (Data_mode == 'y'):
        # OLAP_cube(features_norm, result_df)
        OLAP_3D(features_norm, result_df)

    return result_df


def OLAP_cube(features_normalized, score):

    # --------------------- OLAP_cube ----------------------

    xg = np.arange(len(features_normalized[1]))

    fig = pylab.figure()
    ax = fig.add_subplot(projection='3d')
    for index, line in enumerate(features_normalized):
        ax.bar(xg, line, index+1, zdir='y', color=np.random.rand(3,))
    ax.set_xlabel('Alternatives')
    ax.set_ylabel('Features')
    ax.set_zlabel('Normalized value')
    pylab.show()

    return


def OLAP_3D(features_normalized, score_df):
    feat = features_normalized
    xpos = np.arange(feat.shape[0])
    ypos = np.arange(feat.shape[1])
    yposM, xposM = np.meshgrid(ypos + 0.5, xpos + 0.5)
    zpos = np.zeros(feat.shape).flatten()

    dx = 0.5 * np.ones_like(zpos)
    dy = 0.4 * np.ones_like(zpos)
    dz = feat.ravel()

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    clr = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(feat.shape[1])]
    colors = clr * feat.shape[0]

    ax.bar3d(xposM.ravel(), yposM.ravel(), zpos, dx, dy, dz, color=colors)

    ticks_x = np.arange(feat.shape[1])
    ax.set_xticks(ticks_x)

    ax.set_xlabel('Alternatives')
    ax.set_ylabel('Features')
    ax.set_zlabel('Normalized value')
    plt.xticks(ticks_x, score_df['currency'].to_list())

    plt.show()

# -------------------------------- БЛОК ГОЛОВНИХ ВИКЛИКІВ ------------------------------
if __name__ == '__main__':

    File_name = 'data/result.csv'
    # line_column_matrix = matrix_generation(File_name)


    # ---------------- коефіціенти переваги критеріїв -----------------
    criteria_preference_coefficients_list = np.ones(9)

    print('All alternatives and their scores are next:')
    scores_df = Voronin(File_name, criteria_preference_coefficients_list)
    print(scores_df)
    print('Based on information above we recommend you to consider'
          ' the following currency(ies) for long term investments:')
    print(scores_df[scores_df['if_best']])
    print('And now is appropriate time to buy such assets!')
