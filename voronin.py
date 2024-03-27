import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler, Normalizer

from glossary import criteria
from cube import *

def Voronin(File_name, criteria_coef):
    """
        Compute the scores of alternatives using the convolution criterion.

        This function calculates the scores of alternatives based on a matrix of criteria and
        alternatives from a specified file using the convolution criterion method. The function normalizes the
        data, computes integrated scores, and returns a DataFrame with scores and best alternatives.

        Parameters:
        - File_name (str): The path to the file containing criteria and alternatives data.
        - criteria_coef (numpy.ndarray): Coefficients of criteria importance.

        Returns:
        - pandas.DataFrame: DataFrame containing alternatives, scores, and whether they are the best.
    """
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

    # additional normalization for last feature due to the data specifics
    scaler = MinMaxScaler()
    scaler.fit(features_norm[13].reshape(-1, 1))
    features_norm[13] = scaler.transform(features_norm[13].reshape(-1, 1)).reshape(1, -1)

    # changing features->max to the 1/feature
    for index, opt_direction in enumerate(criteria['optimize']):
        if opt_direction == 'max':
            features_norm[index] = np.divide(1,
                                             features_norm[index],
                                             out=np.zeros_like(features_norm[index]),
                                             where=features_norm[index]!=0)
            # features_norm[index] = 1 / features_norm[index]

    # features normalization
    features_norm_sum = features_norm.sum(axis=1)
    features_norm = np.divide(features_norm.T,
                              features_norm_sum,
                              out=np.zeros_like(features_norm.T),
                              where=features_norm_sum!=0)
    # features_norm = np.divide(features_norm.T, features_norm_sum)
    features_norm = features_norm.T

    # calculating integrated score in few steps
    integro_1 = features_norm.T
    integro_2 = (1 - integro_1)
    integro_3 = np.power(integro_2, (-1))
    integro_4 = integro_3 * criteria_coef_norm
    integro_5 = integro_4.sum(axis=1)

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


def Voronin_sklearn(File_name, criteria_coef):
    """
        Compute the scores of alternatives using the convolution criterion.

        This function calculates the scores of alternatives based on a matrix of criteria and
        alternatives from a specified file using the convolution criterion method. The function normalizes the
        data using the Normalizer from sklearn, computes integrated scores, and returns a
        DataFrame with scores and best alternatives.

        Parameters:
        - File_name (str): The path to the file containing criteria and alternatives data.
        - criteria_coef (numpy.ndarray): Coefficients of criteria importance.

        Returns:
        - pandas.DataFrame: DataFrame containing alternatives, scores, and whether they are the best.
    """
    # --------------------- вхідні дані -------------------------
    line_column_matrix = matrix_generation(File_name)
    features_number = np.shape(line_column_matrix)[0]
    alternatives_number = np.shape(line_column_matrix)[1]
    alternatives = alternatives_names(File_name)

    # --------------- нормалізація вхідних даних ------------------
    scaler = Normalizer()

    # copying features for normalization
    features_norm = np.copy(line_column_matrix)

    # criteria coefficients normalization
    criteria_coef_norm = criteria_coef / criteria_coef.sum()

    # changing features->max to the 1/feature
    for index, opt_direction in enumerate(criteria['optimize']):
        if opt_direction == 'max':
            features_norm[index] = np.divide(1,
                                             features_norm[index],
                                             out=np.zeros_like(features_norm[index]),
                                             where=features_norm[index] != 0)

    # features normalization
    features_norm = scaler.fit_transform(features_norm)

    # calculating integrated score in few steps
    integro_1 = features_norm.T
    integro_2 = (1 - integro_1)
    integro_3 = np.power(integro_2, (-1))
    integro_4 = integro_3 * criteria_coef_norm
    integro_5 = integro_4.sum(axis=1)

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


def matrix_generation(File_name):
    """
        Generate a matrix from a CSV file.

        This function reads a CSV file, drops the first column, and converts the
        remaining data into a numpy array.

        Parameters:
        - File_name (str): The path to the CSV file.

        Returns:
        - numpy.ndarray: A matrix containing the data from the CSV file.
    """
    sample_data_df = pd.read_csv(File_name)
    sample_data_df.drop(columns=sample_data_df.columns[0], axis=1, inplace=True)
    line_column_matrix = sample_data_df.to_numpy()

    return line_column_matrix


def alternatives_names(File_name):
    """
        Extract alternative names from a CSV file.

        This function reads a CSV file to extract the column names, removes the
        first column name, and returns the remaining column names as a list.

        Parameters:
        - File_name (str): The path to the CSV file.

        Returns:
        - list: A list of alternative names.
    """
    sample_data_df = pd.read_csv(File_name)
    header = list(sample_data_df.columns)
    header.pop(0)
    return header