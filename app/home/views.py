from flask import render_template, abort
from flask_login import login_required, current_user


from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template one the / route
    :return: index.html rendered
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    :return: dashboard.html rendered
    """
    return render_template('home/dashboard.html', title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/dept1/dashboard')
@login_required
def dept1_dashboard():
    if current_user.department.id != 1:
        abort(403)
    return render_template('home/dept1_dashboard.html', title="Dashboard for Dept1")

