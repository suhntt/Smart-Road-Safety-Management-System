from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response
from extensions import mysql
from utils.analysis import get_dashboard_data
from utils.forecast import forecast_accidents
import MySQLdb.cursors

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/official', methods=['GET', 'POST'])
def official_dashboard():
    if session.get('role') not in ['doctor', 'police', 'admin', 'teacher', 'army']:
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Handle new point submission
    if request.method == 'POST':
        grid_id = request.form.get('grid_id')
        lat = request.form.get('latitude')
        lng = request.form.get('longitude')

        if grid_id and lat and lng:
            cur.execute("INSERT INTO accidents (state_name, district_name, grid_id, latitude, longitude, total_accidents, year_of_accident) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        ('Assam', 'Dibrugarh', grid_id, lat, lng, 0, 2025))
            mysql.connection.commit()
            flash("New accident-prone area added!", "success")
            return redirect(url_for('dashboard.official_dashboard'))

    # Get data from analysis.py using the DictCursor
    dashboard_data = get_dashboard_data(cur)
    cur.close()

    # Get forecast data from forecast.py using Random Forest ML model
    forecast_data = forecast_accidents(method='rf', future_years=[2026, 2027, 2028], district='Dibrugarh')
    weather_risk = forecast_data.get('weather_risk', {})

    response = make_response(render_template(
        'dashboard_official.html',
        years=dashboard_data['years'] or [],
        total_per_year=dashboard_data['total_per_year'] or [],
        percent_change=dashboard_data['percent_change'] or [],
        highest_year=dashboard_data['highest_year'] or '',
        lowest_year=dashboard_data['lowest_year'] or '',
        highest_value=dashboard_data['highest_value'] or 0,
        lowest_value=dashboard_data['lowest_value'] or 0,
        top_grids=dashboard_data['top_grids_labels'] or [],
        top_grids_labels=dashboard_data['top_grids_labels'] or [],
        top_grids_values=dashboard_data['top_grids_values'] or [],
        grid_trends=dashboard_data['grid_trends'] or [],
        forecast_years=forecast_data['years'] or [],
        forecast_values=forecast_data['values'] or [],
        map_points=dashboard_data['map_points'] or [],
        summary_points=dashboard_data['summary'] or [],
        weather_risk=weather_risk
    ))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
