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

from glossary import criteria


def matrix_generation(File_name):
    sample_data_df = pd.read_csv(File_name)
    sample_data_df.drop(columns=sample_data_df.columns[0], axis=1, inplace=True)
    line_column_matrix = sample_data_df.to_numpy()

    return line_column_matrix


def Voronin(File_name, criteria_coef):
    # --------------------- вхідні дані -------------------------
    line_column_matrix = matrix_generation(File_name)
    features_number = np.shape(line_column_matrix)[0]
    alternatives_number = np.shape(line_column_matrix)[1]
    Integro = np.zeros(alternatives_number)

    # --------------- нормалізація вхідних даних ------------------
    features_norm = np.copy(line_column_matrix)

    criteria_coef_norm = criteria_coef / criteria_coef.sum()

    for index, opt_direction in enumerate(criteria['optimize']):
        if opt_direction == 'max':
            features_norm[index] = 1 / features_norm[index]

    features_norm_sum = features_norm.sum(axis=1)

    features_norm = np.divide(features_norm.T, features_norm_sum).T

    integro_1 = features_norm.T

    integro_2 = (1 - integro_1)

    integro_2_1 = np.power(integro_2, (-1))

    integro_3 = integro_2_1 * criteria_coef_norm

    integro_4 = integro_3.sum(axis=1)

    print(integro_4)

    # Integro[i] = (G10*(1 - F10[i]) ** (-1)) + (G20*(1 - F20[i]) ** (-1)) + (G30*(1 - F30[i]) ** (-1))
    #     + (G40 * (1 - F40[i]) ** (-1)) + (G50 * (1 - F50[i]) ** (-1)) + (G60 * (1 - F60[i]) ** (-1))
    #     + (G70*(1 - F70[i]) ** (-1)) + (G80*(1 - F80[i]) ** (-1)) + (G90*(1 - F90[i]) ** (-1))
    #
    # # --------------- генерація оптимального рішення ----------------
    # min = 10000
    # opt = 0
    # for i in range(column_matrix[1]):
    #     if min > Integro[i]:
    #         min = Integro[i]
    #         opt = i
    # print('Інтегрована оцінка (scor):')
    # print(Integro)
    # print('Номер_оптимального_товару:', opt)

    return


def OLAP_cube(File_name, G1, G2, G3, G4, G5, G6, G7, G8, G9):
    # --------------------- вхідні дані -------------------------
    line_column_matrix = matrix_generation(File_name)
    column_matrix = np.shape(line_column_matrix)
    Integro = np.zeros((column_matrix[1]))

    F1 = line_column_matrix[0]
    F2 = line_column_matrix[1]
    F3 = line_column_matrix[2]
    F4 = line_column_matrix[3]
    F5 = line_column_matrix[4]
    F6 = line_column_matrix[5]
    F7 = line_column_matrix[6]
    F8 = line_column_matrix[7]
    F9 = line_column_matrix[8]

    # --------------- нормалізація вхідних даних ------------------
    F10 = np.zeros((column_matrix[1]))
    F20 = np.zeros((column_matrix[1]))
    F30 = np.zeros((column_matrix[1]))
    F40 = np.zeros((column_matrix[1]))
    F50 = np.zeros((column_matrix[1]))
    F60 = np.zeros((column_matrix[1]))
    F70 = np.zeros((column_matrix[1]))
    F80 = np.zeros((column_matrix[1]))
    F90 = np.zeros((column_matrix[1]))

    GNorm = G1 + G2 + G3 + G4 + G5 + G6 + G7 + G8 + G9
    G10 = G1 / GNorm
    G20 = G2 / GNorm
    G30 = G3 / GNorm
    G40 = G4 / GNorm
    G50 = G5 / GNorm
    G60 = G6 / GNorm
    G70 = G7 / GNorm
    G80 = G8 / GNorm
    G90 = G9 / GNorm

    sum_F1 = sum_F2 = sum_F3 = sum_F4 = sum_F5 = sum_F6 = sum_F7 = sum_F8 = sum_F9 = 0

    for i in range(column_matrix[1]):
        sum_F1 = sum_F1 + F1[i]
        sum_F2 = sum_F2 + (1 / F2[i])
        sum_F3 = sum_F3 + (1 / F3[i])
        sum_F4 = sum_F4 + (1 / F4[i])
        sum_F5 = sum_F5 + (1 / F5[i])
        sum_F6 = sum_F6 + F6[i]
        sum_F7 = sum_F7 + F7[i]
        sum_F8 = sum_F8 + (1 / F8[i])
        sum_F9 = sum_F9 + (1 / F9[i])

    for i in range(column_matrix[1]):
        # --------------- нормалізація критеріїв ------------------
        F10[i] = F1[i] / sum_F1
        F20[i] = (1 / F2[i]) / sum_F2
        F30[i] = (1 / F3[i]) / sum_F3
        F40[i] = (1 / F4[i]) / sum_F4
        F50[i] = (1 / F5[i]) / sum_F5
        F60[i] = F6[i] / sum_F6
        F70[i] = F7[i] / sum_F7
        F80[i] = (1 / F8[i]) / sum_F8
        F90[i] = (1 / F9[i]) / sum_F9

        print('---------------')
        print((G10 * ((1 - F10[i]) ** (-1))), (G20 * ((1 - F20[i]) ** (-1))), (G30 * ((1 - F30[i]) ** (-1))),
              (G40 * ((1 - F40[i]) ** (-1))), (G50 * ((1 - F50[i]) ** (-1))), (G60 * ((1 - F60[i]) ** (-1))),
              (G70 * ((1 - F70[i]) ** (-1))), (G80 * ((1 - F80[i]) ** (-1))), (G90 * ((1 - F90[i]) ** (-1))))

        Integro[i] = (G10 * ((1 - F10[i]) ** (-1))) + (G20 * ((1 - F20[i]) ** (-1))) + (G30 * ((1 - F30[i]) ** (-1)))
        + (G40 * ((1 - F40[i]) ** (-1))) + (G50 * ((1 - F50[i]) ** (-1))) + (G60 * ((1 - F60[i]) ** (-1)))
        + (G70 * ((1 - F70[i]) ** (-1))) + (G80 * ((1 - F80[i]) ** (-1))) + (G90 * ((1 - F90[i]) ** (-1)))
        #
        # Integro[i] += G10*((1 - F10[i]) ** (-1))
        # Integro[i] += G20*((1 - F20[i]) ** (-1))
        # Integro[i] += G30*((1 - F30[i]) ** (-1))
        # Integro[i] += G40*((1 - F40[i]) ** (-1))
        # Integro[i] += G50*((1 - F50[i]) ** (-1))
        # Integro[i] += G60*((1 - F60[i]) ** (-1))
        # Integro[i] += G70*((1 - F70[i]) ** (-1))
        # Integro[i] += G80*((1 - F80[i]) ** (-1))
        # Integro[i] += G90*((1 - F90[i]) ** (-1))

    print(Integro)

    # # --------------------- OLAP_cube ----------------------
    #
    # xg = np.ones((column_matrix[1]))
    # for i in range(len(F10)):
    #     xg[i] = i
    #
    # fig = pylab.figure()
    # ax = fig.add_subplot(projection='3d')
    # clr = ['#4bb2c5', '#c5b47f', '#EAA228', '#579575', '#839557', '#958c12', '#953579', '#4b5de4', '#4bb2c5']
    # ax.bar(xg, F10, 1, zdir='y', color=clr)
    # ax.bar(xg, F20, 2, zdir='y', color=clr)
    # ax.bar(xg, F30, 3, zdir='y', color=clr)
    # ax.bar(xg, F40, 4, zdir='y', color=clr)
    # ax.bar(xg, F50, 5, zdir='y', color=clr)
    # ax.bar(xg, F60, 6, zdir='y', color=clr)
    # ax.bar(xg, F70, 7, zdir='y', color=clr)
    # ax.bar(xg, F80, 8, zdir='y', color=clr)
    # ax.bar(xg, F90, 9, zdir='y', color=clr)
    # ax.bar(xg, Integro, 10, zdir='y', color=clr)
    # ax.set_xlabel('X Label')
    # ax.set_ylabel('Y Label')
    # ax.set_zlabel('Z Label')
    # pylab.show()

    return


# -------------------------------- БЛОК ГОЛОВНИХ ВИКЛИКІВ ------------------------------
if __name__ == '__main__':
    # File_name = 'Pr1.xls'
    File_name = 'data/result.csv'
    line_column_matrix = matrix_generation(File_name)

    # ---------------- коефіціенти переваги критеріїв -----------------
    criteria_preference_coefficients_list = np.ones(9)

    Voronin(File_name, criteria_preference_coefficients_list)
    OLAP_cube(File_name, 1, 1, 1, 1, 1, 1, 1, 1, 1)

    # print('Будувати OLAP_cube:')
    # print('1 - так')
    # print('2 - ні')
    # Data_mode = int(input('mode:'))
    #
    # if (Data_mode == 1):
    #     OLAP_cube(File_name, G1, G2, G3, G4, G5, G6, G7, G8, G9)
    #
    # if(Data_mode == 2):
    #     sys.exit()
