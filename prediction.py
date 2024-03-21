import numpy as np

from datetime import datetime

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.impute import SimpleImputer


def regr_pred(data):
    X = np.arange(len(data))
    pred_length = 7
    X_p = np.arange(len(data)+pred_length)
    shape = len(X_p)
    Y = data

    if np.isnan(Y).any():
        # Impute missing values with mean
        imputer = SimpleImputer(strategy='mean')
        Y = imputer.fit_transform(Y.reshape(-1, 1))

    poly = PolynomialFeatures(degree=4, include_bias=False)
    poly_features = poly.fit_transform(X.reshape(-1, 1))
    poly_features_extra = poly.fit_transform(X_p.reshape(-1, 1))
    poly_reg_model = LinearRegression()
    poly_reg_model.fit(poly_features, Y)
    y_predicted = poly_reg_model.predict(poly_features_extra)
    y_predicted = y_predicted.reshape(shape, )
    pred_analyse(y_predicted)

    return y_predicted

def pred_analyse(data_pred):
    print(f'Вартість даного активу сьогодні {datetime.now().date()} : {data_pred[-8]} у USD')
    print(f'Очікуеться що через тиждень вартість даного активу буде: {data_pred[-1]} у USD')

    y_std = np.std(data_pred)
    borders = [data_pred[-8]-y_std, data_pred[-8]+y_std]

    if (data_pred[-1] > borders[0] and data_pred[-1] < borders[1]):
        print('Схоже що вартість даного активу суттево не зміниться. Це стабільна інвестиція')
    elif (data_pred[-1] < borders[0]):
        print('Очікуеться що вартість активу знизиться. Можливо вам варто позбутися даного активу')
    elif (data_pred[-1] > borders[1]):
        print('Очікуеться що вартість активу збільшиться. Варто розглянути інвестування в даний актив')
