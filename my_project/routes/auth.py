from flask_login.utils import login_required
from my_project import app
from flask import render_template, redirect, url_for, flash, request
from my_project.forms import RegisterForm, LoginForm
from my_project.models import User
from my_project import db
from flask_login import login_user, logout_user, current_user


@app.route("/register", methods=["GET", "POST"])
def register_page():
    status_code = 200

    if current_user.is_authenticated:
        return redirect(url_for("landing_page"))

    form = RegisterForm()  # get the register form from import at top (Forms.py)
    if request.method == "POST":
        if form.validate_on_submit():  # validators
            user_to_create = User(  # set user_to_create to form data
                username=form.username.data,
                email_address=form.email_address.data,
                password=form.password1.data,
            )
            db.session.add(
                user_to_create
            )  # add and commit user_to_create to the Database, User
            db.session.commit()
            login_user(user_to_create)  # log the user_to_create in
            flash(
                f"Account created succesfully and loged in as {user_to_create.username}",
                category="success",
            )
            return redirect(url_for("landing_page"))
        if (
            form.errors != {}
        ):  # checks for validations erros. if {} is empty the error is raised
            for err_msg in form.errors.values():
                flash(f"Error with creating your account: {err_msg[0]}", category="danger")
                status_code = 400

    return render_template("register.html", page_title="Register", form=form), status_code


# login page
@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()  # get the LoginForm from import at top (Forms.py)
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data
        ).first()  # query the attempted login user by the username (the form input)
        # check if the username and the password
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)  # login success
            flash(
                f"Succesfully logged in as: {attempted_user.username}",
                category="success",
            )
            return redirect(url_for("landing_page"))
        else:  # login failed
            flash(
                "Username and password did not match! Please try again",
                category="danger",
            )
    return render_template("login.html", form=form, page_title="Login")


# logout page
@app.route("/logout")  # logout the current user and return the landing page #default method "GET"
@login_required
def logout_page():
    logout_user()
    flash("Succesfully logged out!", category="info")
    return redirect(url_for("landing_page"))