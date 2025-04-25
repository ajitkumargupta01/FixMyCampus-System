# FixMyCampus - Campus Issue Reporting System

FixMyCampus is a comprehensive web application that allows students to report and track campus infrastructure issues. The system provides an intuitive interface for students to submit problems related to electricity, water, internet, furniture, cleanliness, and other campus facilities.

## Features

- **User Authentication**: Secure login/signup system with password recovery
- **Issue Reporting**: Submit detailed reports about campus infrastructure problems
- **Issue Tracking**: Track the status of reported issues (Pending, In Progress, Resolved)
- **User Profiles**: View and update personal information
- **Dashboard**: Visual analytics of campus-wide issues
- **Admin Panel**: Comprehensive management system for administrators
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop devices

## Technical Stack

- **Backend**: Python Flask
- **Database**: MySQL
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Charts**: Chart.js
- **Icons**: Font Awesome

## Directory Structure

```
/fix_my_campus
├── app.py              # Main Flask application
├── admin.py            # Admin panel application
├── requirements.txt    # Python dependencies
├── static/             # Static files
│   ├── css/            # CSS files
│   │   └── styles.css  # Custom styles
│   ├── js/             # JavaScript files
│   │   ├── main.js     # Main JS functionality
│   │   └── charts.js   # Chart initialization
│   └── images/         # Image files
└── templates/          # HTML templates
    ├── layouts/        # Layout templates
    │   └── base.html   # Base template
    ├── components/     # Reusable components
    │   ├── navbar.html # Navigation bar
    │   └── footer.html # Footer
    ├── admin/          # Admin templates
    │   ├── dashboard.html
    │   ├── login.html
    │   ├── manage_issues.html
    │   ├── user_management.html
    │   └── audit_logs.html
    ├── login.html
    ├── signup.html
    ├── forgot_password.html
    ├── home.html
    ├── profile.html
    ├── change_password.html
    ├── report_issue.html
    ├── my_issues.html
    ├── issue_dashboard.html
    ├── about_campus.html
    ├── help_support.html
    └── about.html
```

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/fix-my-campus.git
cd fix-my-campus
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python app.py
```

4. Run the admin panel (separate server):
```
python admin.py
```

## Database Setup

The application is configured to use a MySQL database. The database connection details are set in the app.py file:

```python
app.config['MYSQL_HOST'] = 'sql12.freesqldatabase.com'
app.config['MYSQL_USER'] = 'sql12774989'
app.config['MYSQL_PASSWORD'] = 'acxEkHFzcu'
app.config['MYSQL_DB'] = 'sql12774989'
```

## User Credentials

For testing purposes:

- **Regular User**:
  - Create a new account through the signup page

- **Admin**:
  - Username: admin@1234
  - Password: 123

## License

This project is licensed under the MIT License - see the LICENSE file for details.