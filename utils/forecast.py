# forecast.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures
import requests

from utils.db import get_db_connection  # Make sure db.py exists in the same folder


def fetch_yearly_totals(district='Dibrugarh'):
    """
    Fetch total accidents per year for a given district.
    Returns a list of dicts with year and total accidents.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT year_of_accident, SUM(total_accidents) AS total
        FROM accidents
        WHERE district_name = %s
        GROUP BY year_of_accident
        ORDER BY year_of_accident
    """, (district,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_live_weather_risk():
    try:
        api_key = '3ba87914cc86b857184893e28fe90adf'
        res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Dibrugarh&appid={api_key}&units=metric", timeout=5)
        data = res.json()
        weather_main = data['weather'][0]['main'].lower()
        desc = data['weather'][0]['description'].title()
        temp = data['main']['temp']
        
        multiplier = 1.0
        risk_level = "Normal"
        
        if 'rain' in weather_main or 'drizzle' in weather_main:
            multiplier = 1.30
            risk_level = "High (+30% Risk)"
        elif 'fog' in weather_main or 'mist' in weather_main or 'haze' in weather_main:
            multiplier = 1.40
            risk_level = "Very High (+40% Risk)"
        elif 'thunderstorm' in weather_main:
            multiplier = 1.50
            risk_level = "Critical (+50% Risk)"
        elif 'clear' in weather_main:
            multiplier = 1.0
            risk_level = "Low (Clear Weather)"
            
        return {
            "condition": desc,
            "temp": temp,
            "multiplier": multiplier,
            "risk_level": risk_level
        }
    except Exception as e:
        return {
            "condition": "Data Unavailable",
            "temp": "--",
            "multiplier": 1.0,
            "risk_level": "Unknown"
        }


def forecast_accidents(method='poly', future_years=[2026, 2027, 2028], district='Dibrugarh'):
    """
    Forecast accident totals using ML models.
    - method: 'linear', 'poly', or 'rf'
    - future_years: list of future years to predict
    - district: name of the district (default 'Dibrugarh')
    
    Returns:
        {
            'years': [2026, 2027, 2028],
            'values': [forecasted_accidents_2026, ..., 2028]
        }
    """
    data = fetch_yearly_totals(district)

    if len(data) < 2:
        last_val = data[-1]['total'] if data else 1000
        return {
            'years': future_years,
            'values': [last_val] * len(future_years)
        }

    # Prepare data for model
    df = pd.DataFrame(data)
    X = df['year_of_accident'].values.reshape(-1, 1)
    y = df['total'].values
    X_future = np.array(future_years).reshape(-1, 1)

    # Apply the selected forecasting method
    if method == 'linear':
        model = LinearRegression()
        model.fit(X, y)
        forecast_y = model.predict(X_future)

    elif method == 'rf':
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        forecast_y = model.predict(X_future)

    elif method == 'poly':
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        forecast_y = model.predict(poly.transform(X_future))

    else:
        raise ValueError("Unknown forecasting method. Use 'linear', 'poly', or 'rf'.")

    # Apply Weather Multiplier to Forecast
    weather = get_live_weather_risk()
    adjusted_forecast = []
    
    # Ensure no negative predictions and apply weather risk to the immediate next year (2026)
    for i, val in enumerate(forecast_y):
        base_val = max(0, int(round(val)))
        if i == 0:  # Current/Upcoming Year Live Risk
            adjusted_forecast.append(int(base_val * weather['multiplier']))
        else:
            adjusted_forecast.append(base_val)

    return {
        'years': future_years,
        'values': adjusted_forecast,
        'weather_risk': weather
    }
