from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import datetime
import pandas as pd
import plotly.express as px
import plotly.utils
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'fixmycampus_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12774989'
app.config['MYSQL_PASSWORD'] = 'acxEkHFzcu'
app.config['MYSQL_DB'] = 'sql12774989'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Authentication routes
@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE roll_no = %s", [roll_no])
        user = cur.fetchone()
        
        if user and user['password'] == password:
            if user['is_banned']:
                flash('Your account has been banned. Please contact admin.', 'danger')
                return render_template('login.html')
            
            session['logged_in'] = True
            session['roll_no'] = user['roll_no']
            session['username'] = f"{user['first_name']} {user['last_name']}"
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        mob_num = request.form['mob_num']
        gender = request.form['gender']
        roll_no = request.form['roll_no']
        
        cur = mysql.connection.cursor()
        try:
            cur.execute(
                "INSERT INTO users (first_name, last_name, email, password, mob_num, gender, roll_no) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (first_name, last_name, email, password, mob_num, gender, roll_no)
            )
            mysql.connection.commit()
            cur.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        mob_num = request.form['mob_num']
        new_password = request.form['new_password']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET password = %s WHERE roll_no = %s AND mob_num = %s", 
                   [new_password, roll_no, mob_num])
        if cur.rowcount > 0:
            mysql.connection.commit()
            flash('Password reset successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash('No matching user found with that Roll Number and Mobile Number.', 'danger')
    
    return render_template('forgot_password.html')

# User routes
@app.route('/home')
def home():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/profile')
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT first_name, last_name, email, mob_num, gender, roll_no FROM users WHERE roll_no = %s", 
               [session['roll_no']])
    user = cur.fetchone()
    cur.close()
    
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    mob_num = request.form['mob_num']
    gender = request.form['gender']
    
    cur = mysql.connection.cursor()
    cur.execute('''
        UPDATE users
        SET first_name = %s, last_name = %s, email = %s, mob_num = %s, gender = %s
        WHERE roll_no = %s
    ''', (first_name, last_name, email, mob_num, gender, session['roll_no']))
    mysql.connection.commit()
    cur.close()
    
    session['username'] = f"{first_name} {last_name}"
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('change_password'))
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT password FROM users WHERE roll_no = %s", [session['roll_no']])
        user = cur.fetchone()
        
        if user['password'] == current_password:
            cur.execute("UPDATE users SET password = %s WHERE roll_no = %s", 
                       [new_password, session['roll_no']])
            mysql.connection.commit()
            cur.close()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Current password is incorrect', 'danger')
    
    return render_template('change_password.html')

# Issue routes
@app.route('/report_issue', methods=['GET', 'POST'])
def report_issue():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        issue_type = request.form['issue_type']
        if issue_type == 'Other':
            issue_type = request.form['custom_issue_type']
        description = request.form['description']
        location = request.form['location']
        status = 'Pending'
        date_reported = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO issues (roll_no, issue_type, description, location, status, date_reported)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (session['roll_no'], issue_type, description, location, status, date_reported))
        mysql.connection.commit()
        cur.close()
        
        flash('Issue reported successfully!', 'success')
        return redirect(url_for('my_issues'))
    
    return render_template('report_issue.html')

@app.route('/my_issues')
def my_issues():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT issue_id, issue_type, description, location, status, date_reported
        FROM issues
        WHERE roll_no = %s
        ORDER BY date_reported DESC
    ''', [session['roll_no']])
    issues = cur.fetchall()
    cur.close()
    
    return render_template('my_issues.html', issues=issues)

@app.route('/issue_dashboard')
def issue_dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT roll_no, issue_id, issue_type, description, location, status, date_reported
        FROM issues
        ORDER BY date_reported DESC
    ''')
    issues = cur.fetchall()
    cur.close()
    
    # Prepare data for charts
    issue_count_by_status = {}
    issue_count_by_category = {}
    
    for issue in issues:
        # Count by status
        status = issue['status']
        if status in issue_count_by_status:
            issue_count_by_status[status] += 1
        else:
            issue_count_by_status[status] = 1
        
        # Count by category
        category = issue['issue_type']
        if category in issue_count_by_category:
            issue_count_by_category[category] += 1
        else:
            issue_count_by_category[category] = 1
    
    return render_template('issue_dashboard.html', issues=issues, 
                          status_data=issue_count_by_status,
                          category_data=issue_count_by_category)

@app.route('/about_campus')
def about_campus():
    return render_template('about_campus.html')

@app.route('/help_support')
def help_support():
    return render_template('help_support.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Admin routes
@app.route('/admin')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin@1234' and password == '123':
        session['admin_logged_in'] = True
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM issues')
    issues = cur.fetchall()
    
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    
    pending_count = sum(1 for issue in issues if issue['status'] == 'Pending')
    in_progress_count = sum(1 for issue in issues if issue['status'] == 'In Progress')
    resolved_count = sum(1 for issue in issues if issue['status'] == 'Resolved')
    
    return render_template('admin/dashboard.html', 
                          issues=issues, 
                          users=users,
                          total_issues=len(issues),
                          pending_count=pending_count,
                          in_progress_count=in_progress_count,
                          resolved_count=resolved_count)

@app.route('/admin/manage_issues')
def admin_manage_issues():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    status_filter = request.args.get('status', 'All')
    roll_no_filter = request.args.get('roll_no', '')
    category_filter = request.args.get('category', '')
    
    cur = mysql.connection.cursor()
    
    query = "SELECT * FROM issues WHERE 1=1"
    params = []
    
    if status_filter != 'All':
        query += " AND status = %s"
        params.append(status_filter)
    
    if roll_no_filter:
        query += " AND roll_no LIKE %s"
        params.append(f"%{roll_no_filter}%")
    
    if category_filter:
        query += " AND issue_type LIKE %s"
        params.append(f"%{category_filter}%")
    
    query += " ORDER BY date_reported DESC"
    
    cur.execute(query, params)
    issues = cur.fetchall()
    cur.close()
    
    return render_template('admin/manage_issues.html', issues=issues, 
                          status_filter=status_filter,
                          roll_no_filter=roll_no_filter,
                          category_filter=category_filter)

@app.route('/admin/update_issue_status', methods=['POST'])
def admin_update_issue_status():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    issue_id = request.form['issue_id']
    new_status = request.form['status']
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE issues SET status = %s WHERE issue_id = %s", [new_status, issue_id])
    mysql.connection.commit()
    
    # Log the action
    action = "Issue Updated"
    details = f"Issue ID: {issue_id}, New Status: {new_status}"
    cur.execute(
        "INSERT INTO audit_logs (action, details, timestamp) VALUES (%s, %s, %s)",
        (action, details, datetime.datetime.now())
    )
    mysql.connection.commit()
    cur.close()
    
    flash('Issue status updated successfully!', 'success')
    return redirect(url_for('admin_manage_issues'))

@app.route('/admin/delete_issue/<int:issue_id>', methods=['POST'])
def admin_delete_issue(issue_id):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM issues WHERE issue_id = %s", [issue_id])
    mysql.connection.commit()
    
    # Log the action
    action = "Issue Deleted"
    details = f"Issue ID: {issue_id}"
    cur.execute(
        "INSERT INTO audit_logs (action, details, timestamp) VALUES (%s, %s, %s)",
        (action, details, datetime.datetime.now())
    )
    mysql.connection.commit()
    cur.close()
    
    flash('Issue deleted successfully!', 'success')
    return redirect(url_for('admin_manage_issues'))

@app.route('/admin/user_management')
def admin_user_management():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    
    return render_template('admin/user_management.html', users=users)

@app.route('/admin/ban_user/<string:roll_no>', methods=['POST'])
def admin_ban_user(roll_no):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_banned = 1 WHERE roll_no = %s", [roll_no])
    mysql.connection.commit()
    
    # Log the action
    action = "User Banned"
    details = f"Roll No: {roll_no}"
    cur.execute(
        "INSERT INTO audit_logs (action, details, timestamp) VALUES (%s, %s, %s)",
        (action, details, datetime.datetime.now())
    )
    mysql.connection.commit()
    cur.close()
    
    flash('User banned successfully!', 'success')
    return redirect(url_for('admin_user_management'))

@app.route('/admin/unban_user/<string:roll_no>', methods=['POST'])
def admin_unban_user(roll_no):
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET is_banned = 0 WHERE roll_no = %s", [roll_no])
    mysql.connection.commit()
    
    # Log the action
    action = "User Unbanned"
    details = f"Roll No: {roll_no}"
    cur.execute(
        "INSERT INTO audit_logs (action, details, timestamp) VALUES (%s, %s, %s)",
        (action, details, datetime.datetime.now())
    )
    mysql.connection.commit()
    cur.close()
    
    flash('User unbanned successfully!', 'success')
    return redirect(url_for('admin_user_management'))

@app.route('/admin/audit_logs')
def admin_audit_logs():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50")
    logs = cur.fetchall()
    cur.close()
    
    return render_template('admin/audit_logs.html', logs=logs)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out', 'info')
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)