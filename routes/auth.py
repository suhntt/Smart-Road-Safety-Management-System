from flask import Blueprint, render_template, request, redirect, url_for, session, flash, make_response, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import mysql, mail
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer

auth_bp = Blueprint('auth', __name__)

def get_serializer():
    return URLSafeTimedSerializer(current_app.secret_key)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            flash("Email already exists. Please use a different one.")
            return redirect(url_for('auth.signup'))

        hashed_password = generate_password_hash(password)
        cur.execute("INSERT INTO users (name, email, password, role, phone, approved) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, email, hashed_password, role, phone, 0))
        mysql.connection.commit()
        cur.close()

        flash("Signup successful. Please wait for admin approval.")
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']

        if email == "admin@roadsafety.in" and password_input == "Admin@123":
            session['user_id'] = 0
            session['name'] = "Super Admin"
            session['role'] = "admin"
            return redirect(url_for('admin.admin_dashboard'))

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, email, password, role, approved FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            user_id, name, email_db, hashed_password, role, approved = user
            if check_password_hash(hashed_password, password_input):
                if approved == 0:
                    flash("Your account is awaiting admin approval.")
                    return redirect(url_for('auth.login'))
                session['user_id'] = user_id
                session['name'] = name
                session['role'] = role
                return redirect(url_for('admin.admin_dashboard') if role == 'admin' else url_for('dashboard.official_dashboard'))
            else:
                flash('Invalid password.')
        else:
            flash('Email not registered.')
    return render_template('login.html')

@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            try:
                s = get_serializer()
                token = s.dumps(email, salt='reset-password')
                link = url_for('auth.reset_with_token', token=token, _external=True)

                msg = Message(
                    'Reset Your Password',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[email]
                )
                msg.body = f"THIS IS DIBRUGARH DISTRICT GOVERNMENT MAIL Click this link to reset your password for Roadsafety web:\n{link}\n\nNote: Link is valid for 10 minutes only."

                mail.send(msg)
                flash('Reset link sent to your email.', 'success')
                return redirect(url_for('auth.login'))

            except Exception as e:
                print("==== EMAIL ERROR ====")
                print(e)
                flash("Failed to send email. Check config or connection.", "danger")
                return redirect(url_for('auth.forgot_password'))
        else:
            flash('No account found with that email.', 'warning')
            return redirect(url_for('auth.forgot_password'))

    return render_template('forgot_password.html')

@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_with_token(token):
    s = get_serializer()
    try:
        email = s.loads(token, salt='reset-password', max_age=600)  # 10 mins
    except Exception as e:
        flash("Reset link is invalid or has expired.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        hashed_pw = generate_password_hash(password)

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_pw, email))
        mysql.connection.commit()
        cur.close()

        flash("Password has been reset successfully. You can now log in.", "success")
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', email=email)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    response = make_response(redirect(url_for('auth.login')))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
