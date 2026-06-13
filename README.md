# 🚦 Smart Road Safety Management System

![Project Banner](static/banner1%20copy.jpg)

**Smart Road Safety Management System** is an advanced, data-driven web application designed to help District Transport Authorities, Police, and Healthcare Officials monitor, analyze, and predict traffic accidents. Built as a B.Tech Final Year Project, it utilizes Machine Learning, live API integrations, and Interactive GIS Mapping to transition road safety management from reactive to predictive.

---

## ✨ Key Features

*   **🤖 AI Public Assistant Chatbot:** A custom-built NLP chatbot integrated directly into the homepage to assist citizens with traffic rules, emergency contacts, and accident reporting guidelines.
*   **📈 Machine Learning Accident Forecasting:** Utilizes Scikit-Learn's `RandomForestRegressor` and `PolynomialFeatures` to analyze historical accident data and predict future trends for 2026–2028.
*   **🌧️ Live Weather-Adjusted Risk ML:** Dynamically pulls live weather data from OpenWeatherMap via API and adjusts the ML accident forecast risk in real-time (e.g., automatically detecting 'Heavy Rain' and applying a +30% risk multiplier).
*   **🗺️ Interactive GIS Heatmap:** Integrates Leaflet.js to plot accident hotspots geographically, allowing officials to visually pinpoint the most dangerous grids in the district.
*   **🔐 Role-Based Access Control (RBAC):** Secure login portals tailored for distinct roles: Admin, Police, Doctors, Teachers, and Army officials. Only verified, Admin-approved users can access the Official Dashboard.
*   **📊 Dynamic Charting & PDF Reporting:** Generates dynamic, theme-aware visualizations using `Chart.js`, with the ability to instantly export the dashboard to a formal PDF report using `html2pdf.js`.
*   **🌓 Modern UI with Light/Dark Mode:** Features a stunning, fully responsive interface built with pure CSS variables, ensuring high contrast and readability across devices without relying on heavy frontend frameworks.

---

## 🛠️ Technology Stack

*   **Backend:** Python 3, Flask, Flask-Mail, Flask-MySQLdb
*   **Frontend:** HTML5, CSS3, Vanilla JavaScript, Jinja2
*   **Database:** MySQL
*   **Machine Learning:** Scikit-Learn, Pandas, Numpy
*   **Third-Party Libraries/APIs:** Leaflet.js (GIS), Chart.js (Data Vis), html2pdf.js (Reporting), OpenWeatherMap (Live Weather)

---

## 🚀 Installation & Local Setup

Follow these steps to run the project locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/suhntt/Smart-Road-Safety-Management-System.git
   cd Smart-Road-Safety-Management-System
   ```

2. **Set up the Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Database & Environment:**
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
   - Update `config.py` and `app.py` with your MySQL user/password.

5. **Run the Application:**
   ```bash
   python app.py
   ```
   *The server will start at `http://127.0.0.1:5000`.*

---

## 👨‍💻 Developed By

**Sushanta Chetry**  
*B.Tech Final Year Industrial Project*  
Focused on bringing modern AI and data science solutions to critical public sector infrastructure.
