from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from google.cloud import logging
from .forms import LoginForm
from .models import User
from . import db

logging_client = logging.Client()
log = logging_client.logger("flask-app-template")
auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@auth.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        if not user:
            log.log_struct(
                {
                    "message": f"Login error (user does not exist): {email}",
                    "event_id": 110,
                    "user": email,
                },
                severity="INFO",
            )
        elif not check_password_hash(user.password, password):
            log.log_struct(
                {
                    "message": f"Login error (incorrect password): {email}",
                    "event_id": 110,
                    "user": email,
                },
                severity="INFO",
            )
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    form = LoginForm()
    if form.validate_on_submit():
        log.log_struct(
            {"message": f"Login: {user.email}", "event_id": 100, "user": user.email},
            severity="INFO",
        )
        login_user(user, remember=remember)

    return redirect(url_for("main.profile"))


@auth.route("/signup")
def signup():
    form = LoginForm()
    return render_template("signup.html", form=form)


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists")
        return redirect(url_for("auth.signup"))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method="sha256"),
    )
    db.session.add(new_user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        log.log_text(
            f"Failure adding user to database: {new_user.email}", severity="ERROR"
        )
        flash(
            "There was an error with your request. Please try again later or contact IT."
        )
        return redirect(url_for("auth.signup"))

    log.log_struct(
        {
            "message": f"New user: {new_user.email}",
            "event_id": 120,
            "user": new_user.email,
        },
        severity="INFO",
    )
    return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    log.log_struct(
        {
            "message": f"Logout: {current_user.email}",
            "event_id": 130,
            "user": current_user.email,
        }
    )
    logout_user()
    return redirect(url_for("main.index"))
