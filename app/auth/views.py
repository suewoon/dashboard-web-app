from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Insert an employee to the database through the registration form
    :return: Response for sign up if it was successful,
    else HTML rendered register form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.username.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # insert into db
        db.session.add(employee)
        db.session.commit()
        flash("Thanks! You have successfully signed up to DataMatters! You may now login. ")

        # redirect
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Verify an user through the login form
    :return: Response for log in if it was successful,
    else HTML rendered login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            login_user(employee)

            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            elif employee.department.id == 1:
                return redirect(url_for('home.dept1_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))

        else:
            flash("Invalid email or password")

    return render_template("auth/login.html", form=form, title="Login")

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log and employee out through the logout link
    :return:
    """
    logout_user()
    flash("You have successfully been logged out.")

    return redirect(url_for('auth.login'))
