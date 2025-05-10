from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

def polynomial_regression(x, y, degree=3):
    poly_features = PolynomialFeatures(degree=degree)
    x_poly = poly_features.fit_transform(x.reshape(-1, 1))
    
    model = LinearRegression()
    model.fit(x_poly, y)
    
    return model

def predict_with_polynomial(model, x):
    poly_features = PolynomialFeatures(degree=model.n_features_in_ - 1)
    x_poly = poly_features.fit_transform(x.reshape(-1, 1))
    
    return model.predict(x_poly)

def perform_polynomial_regression(months, prices, degree=3, predict_month=None):
    """
    Melakukan regresi polinomial pada data harga beras.
    Args:
        months (list): List bulan (bisa dalam bentuk angka, misal 2024.5 untuk Juni 2024)
        prices (list): List harga
        degree (int): Derajat polinomial
        predict_month (float): Bulan yang ingin diprediksi (misal 2025.25 untuk April 2025)
    Returns:
        float: Harga prediksi untuk bulan yang diminta
    """
    if len(months) < degree + 1:
        raise ValueError("Data tidak cukup untuk regresi polinomial.")
    coeffs = np.polyfit(months, prices, degree)
    poly = np.poly1d(coeffs)
    if predict_month is not None:
        return float(poly(predict_month))
    return poly