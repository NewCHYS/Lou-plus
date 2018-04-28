from flask import flash
from flask import Blueprint, render_template, redirect, url_for
from flask import request, current_app
from flask_login import login_user, logout_user, login_required

from jobplus.forms import LoginForm, RegisterForm
from jobplus.models import User, Company, Job


front = Blueprint("front", __name__)


@front.route("/")
def index():
    page = request.args.get('page', default=1, type=int)

    pagination = Job.query.filter_by(online=True).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    pagination2 = Company.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template("index.html", pagination=pagination, pagination2=pagination2)


@front.route("/reg_company", methods=['GET', 'POST'])
def company_register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user(20)
        flash('Company register success', 'success')
        return redirect(url_for('.login'))
    return render_template("reg_company.html", form=form)


@front.route("/reg_jobseeker", methods=['GET', 'POST'])
def jobseeker_register():
    form = RegisterForm()
    if form.validate_on_submit():
        form.create_user(10)
        flash('Jobseeket register success', 'success')
        return redirect(url_for('.login'))
    return render_template("reg_jobseeker.html", form=form)


@front.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for(".index"))

    return render_template("login.html", form=form)


@front.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout success", "success")
    return redirect(url_for(".index"))
