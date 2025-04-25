from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_mysqldb import MySQL
import datetime
import pandas as pd

app = Flask(__name__)
app.secret_key = 'fixmycampus_admin_secret_key'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12774989'
app.config['MYSQL_PASSWORD'] = 'acxEkHFzcu'
app.config['MYSQL_DB'] = 'sql12774989'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def admin_login():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/login.html')

@app.route('/login', methods=['POST'])
def admin_login_post():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin@1234' and password == '123':
        session['admin_logged_in'] = True
        flash('Login successful!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('Invalid credentials', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/dashboard')
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

@app.route('/manage_issues')
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

@app.route('/update_issue_status', methods=['POST'])
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

@app.route('/delete_issue/<int:issue_id>', methods=['POST'])
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

@app.route('/user_management')
def admin_user_management():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    
    return render_template('admin/user_management.html', users=users)

@app.route('/ban_user/<string:roll_no>', methods=['POST'])
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

@app.route('/unban_user/<string:roll_no>', methods=['POST'])
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

@app.route('/audit_logs')
def admin_audit_logs():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 50")
    logs = cur.fetchall()
    cur.close()
    
    return render_template('admin/audit_logs.html', logs=logs)

@app.route('/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Admin logged out', 'info')
    return redirect(url_for('admin_login'))

@app.route('/api/data/issues_by_date')
def issues_by_date():
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT date_reported FROM issues ORDER BY date_reported')
    issues = cur.fetchall()
    cur.close()
    
    if not issues:
        return jsonify({'dates': [], 'counts': []})
    
    # Convert to pandas DataFrame for easier grouping
    df = pd.DataFrame(issues)
    df['date_reported'] = pd.to_datetime(df['date_reported']).dt.date
    
    # Group by date and count
    grouped = df.groupby('date_reported').size().reset_index(name='count')
    
    return jsonify({
        'dates': [d.strftime('%Y-%m-%d') for d in grouped['date_reported']],
        'counts': grouped['count'].tolist()
    })

if __name__ == '__main__':
    app.run(debug=True, port=8504)