from scipy.interpolate import CubicSpline
import numpy as np

def smooth_data(months, prices):
    if len(months) < 2:
        raise ValueError("Not enough data points to perform cubic spline interpolation.")
    
    spline = CubicSpline(months, prices, bc_type='natural')
    smoothed_prices = spline(months)
    
    return smoothed_prices

def interpolate_historical_data(historical_data):
    smoothed_data = {}
    
    for quality, (months, prices) in historical_data.items():
        smoothed_prices = smooth_data(months, prices)
        smoothed_data[quality] = (months, smoothed_prices)
    
    return smoothed_data
def perform_cubic_spline_interpolation(months, prices, predict_month):
    """
    Melakukan interpolasi cubic spline pada data harga beras.
    Args:
        months (list): List bulan (misal: [2023.0, 2023.083, ...])
        prices (list): List harga
        predict_month (float): Bulan yang ingin diprediksi (misal 2025.25 untuk April 2025)
    Returns:
        float: Harga hasil interpolasi untuk bulan yang diminta
    """
    if len(months) < 2:
        raise ValueError("Not enough data points to perform cubic spline interpolation.")
    spline = CubicSpline(months, prices, bc_type='natural')
    return float(spline(predict_month))