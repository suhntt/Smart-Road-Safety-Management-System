# Smart Road Safety Management System

A web-based system designed to help Transport Authorities, Police, and Healthcare Officials monitor and analyze traffic accidents in Dibrugarh. This project was developed as a B.Tech Final Year Industrial Project. It uses machine learning and interactive mapping to analyze road safety data.

## Features

- **Public Assistant Chatbot:** A local NLP chatbot that assists citizens with traffic rules, emergency contacts, and guidelines.
- **Accident Forecasting:** Uses Random Forest regression to analyze historical accident data and predict future trends (2026-2028).
- **Weather Integration:** Fetches live weather data from OpenWeatherMap to dynamically adjust the accident forecast risk.
- **Interactive GIS Map:** Uses Leaflet.js to plot accident hotspots geographically.
- **Role-Based Access Control:** Distinct login portals for Admin, Police, Doctors, Teachers, and Army officials.
- **Data Export:** Generate PDF reports from the official dashboard.

## Technology Stack

- **Backend:** Python 3, Flask, Flask-Mail, Flask-MySQLdb
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL
- **Machine Learning:** Scikit-Learn, Pandas, Numpy

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/suhntt/Smart-Road-Safety-Management-System.git
   cd Smart-Road-Safety-Management-System
   ```

2. **Set up the virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database & Environment Setup:**
   - Install MySQL and create a database named `roadsafety`.
   - Create a `.env` file in the root directory and add your credentials:
     ```env
     SECRET_KEY=your_secret_flask_key
     MAIL_SERVER=smtp.gmail.com
     MAIL_PORT=587
     MAIL_USE_TLS=True
     MAIL_USERNAME=your_email@gmail.com
     MAIL_PASSWORD=your_app_password
     ```
   - Update `config.py` and `app.py` with your MySQL connection details.

5. **Run the server:**
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

## Developer

Developed by Sushanta Chetry for B.Tech Final Year Industrial Project.
