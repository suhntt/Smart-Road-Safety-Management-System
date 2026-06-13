from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
import pandas as pd
import numpy as np
from extensions import mysql, mail
from flask_mail import Message

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name, email, role FROM users WHERE approved = 0")
    pending_users = cur.fetchall()
    cur.close()

    pending_user_list = [{"id": row[0], "name": row[1], "email": row[2], "role": row[3]} for row in pending_users]
   
    response = make_response(render_template('dashboard_admin.html', pending_users=pending_user_list))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@admin_bp.route('/approved_users')
def approved_users():
    if session.get('role') != 'admin':
        flash('Access denied.')
        return redirect(url_for('auth.login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT name, email, phone, role FROM users WHERE approved = 1")
    users = cur.fetchall()
    cur.close()

    return render_template('approved_users.html', users=users)

@admin_bp.route('/approve_user/<int:user_id>', methods=['GET', 'POST'])
def approve_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    try:
        cur = mysql.connection.cursor()

        # Step 1: Approve the user in DB
        cur.execute("UPDATE users SET approved = 1 WHERE id = %s", (user_id,))
        mysql.connection.commit()

        # Step 2: Fetch user details for email
        cur.execute("SELECT email, name FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if user:
            email, name = user

            # Step 3: Send mail
            msg = Message("Account Approved",
                          sender=current_app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f"""
Hello {name},

✅ Your account has been approved by the Dibrugarh District Government.

You can now log in at: {url_for('auth.login', _external=True)}

Best regards,  
District Admin Team
"""
            mail.send(msg)
            flash("User approved and email sent!", "success")
        else:
            flash("User not found!", "danger")

    except Exception as e:
        print("=== EMAIL SENDING FAILED ===")
        print(e)
        flash("User approved but failed to send email. Please check your email configuration.", "warning")

    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/reject_user/<int:user_id>',  methods=['GET', 'POST'])
def reject_user(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    mysql.connection.commit()
    cur.close()
    flash("User rejected and removed.")
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/upload', methods=['POST'])
def upload_excel():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))

    file = request.files['file']
    if file.filename.endswith('.xlsx'):
        df = pd.read_excel(file)
        df = df.replace({np.nan: None})

        cur = mysql.connection.cursor()
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO accidents (
                    state_name, district_name, latitude, longitude, grid_id,
                    total_accidents, year_of_accident, `rank`, ambulance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row['State name'], row['District name'], row['Lat'], row['Long'], row['Grid ID'],
                row['Total Accidents'], row['Year of Accident'], row['Rank'], row['Ambulance']
            ))
        mysql.connection.commit()
        cur.close()
        flash('Excel data uploaded successfully')

    return redirect(url_for('admin.admin_dashboard'))
