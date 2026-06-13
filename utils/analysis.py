def get_dashboard_data(cursor):
    cursor.execute("""
        SELECT year_of_accident, SUM(total_accidents) as total
        FROM accidents
        WHERE district_name = 'Dibrugarh'
        GROUP BY year_of_accident ORDER BY year_of_accident
    """)
    yearly_data = cursor.fetchall()
    years = [row['year_of_accident'] for row in yearly_data]
    total_per_year = [row['total'] for row in yearly_data]

    # YoY % Change
    percent_change = [0]
    for i in range(1, len(total_per_year)):
        change = ((total_per_year[i] - total_per_year[i-1]) / total_per_year[i-1]) * 100
        percent_change.append(round(change, 2))

    highest_value = max(total_per_year)
    lowest_value = min(total_per_year)
    highest_year = years[total_per_year.index(highest_value)]
    lowest_year = years[total_per_year.index(lowest_value)]

    # Top 5 Grids
    cursor.execute("""
        SELECT grid_id, SUM(total_accidents) AS total FROM accidents
        WHERE district_name = 'Dibrugarh'
        GROUP BY grid_id ORDER BY total DESC LIMIT 5
    """)
    top_grids = cursor.fetchall()
    top_grids_labels = [row['grid_id'] for row in top_grids]
    top_grids_values = [row['total'] for row in top_grids]

    # Grid Trends (per year)
    grid_trends = []
    colors = ['#ff0000', '#00cc66', '#3366ff', '#ffcc00', '#9933ff']
    for i, grid in enumerate(top_grids):
        cursor.execute("""
            SELECT year_of_accident, SUM(total_accidents) AS total FROM accidents
            WHERE district_name = 'Dibrugarh' AND grid_id = %s
            GROUP BY year_of_accident ORDER BY year_of_accident
        """, (grid['grid_id'],))
        rows = cursor.fetchall()
        data = [r['total'] for r in rows]
        grid_trends.append({
            'grid_id': grid['grid_id'],
            'data': data,
            'color': colors[i % len(colors)]
        })

    # Map Points
    cursor.execute("""
        SELECT grid_id, MAX(latitude) as latitude, MAX(longitude) as longitude, SUM(total_accidents) as total
        FROM accidents
        WHERE district_name = 'Dibrugarh'
        GROUP BY grid_id
    """)
    map_points = [{'grid_id': row['grid_id'], 'lat': row['latitude'], 'lng': row['longitude'], 'total': row['total']} for row in cursor.fetchall()]
    top_map_points = sorted(map_points, key=lambda x: x['total'], reverse=True)[:5]

    # Summary
    summary = [
        f"{sum(total_per_year)} total accidents reported between {years[0]} and {years[-1]}",
        f"{highest_year} had the highest accident count with {highest_value} cases.",
        f"{lowest_year} recorded the lowest at {lowest_value} cases.",
        f"Top grids: {', '.join(top_grids_labels)}",
        "Year-on-year changes analyzed and forecasted for better planning.",
    ]

    return {
        'years': years,
        'total_per_year': total_per_year,
        'percent_change': percent_change,
        'highest_year': highest_year,
        'highest_value': highest_value,
        'lowest_year': lowest_year,
        'lowest_value': lowest_value,
        'top_grids_labels': top_grids_labels,
        'top_grids_values': top_grids_values,
        'grid_trends': grid_trends,
        'map_points': map_points,
        'top_map_points': top_map_points,
        'summary': summary
    }
