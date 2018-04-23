from flask import flash
from flask import redirect, url_for
from flask import current_app, request
from flask import Blueprint, render_template
from flask_login import login_required

from jobplus.decorators import admin_required
from jobplus.models import db, User, Company, Jobseeker, Job
from jobplus.forms import UserForm, JobseekerForm, JobForm


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
def index():
    return render_template("admin/index.html")

@admin.route("/userlist")
@admin_required
def userlist():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/userlist.html', pagination=pagination)

@admin.route("/user/create", methods=["GET", "POST"])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('User create success', 'success')
        return redirect(url_for('admin.userlist'))
    return render_template('admin/create_user.html', form=form)

@admin.route("/user/edit/<int:user_id>", methods=["GET", "POST"])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    name = ''
    if user.role == 20:
        name = user.company.name
    elif user.role == 10:
        name = user.jobseeker.name
    else:
        name = ''
    form.name.data = name
    form.password.value = user.password
    if form.validate_on_submit():
        form.update_user(user)
        flash('User update success', 'success')
        return redirect(url_for('admin.userlist'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route("user/change_userstatus/<int:user_id>")
@admin_required
def change_userstatus(user_id):
    user = User.query.get_or_404(user_id)
    user.is_enabled = not user.is_enabled
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.userlist'))

@admin.route("user/delete/<int:user_id>")
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin.userlist'))

@admin.route("joblist")
@admin_required
def joblist():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/joblist.html', pagination=pagination)

@admin.route("/job/create", methods=["GET", "POST"])
@admin_required
def create_job():
    form = JobForm()
    form.update_companylist()
    if form.validate_on_submit():
        form.create_job()
        flash('Job create success', 'success')
        return redirect(url_for('admin.joblist'))
    return render_template('admin/create_job.html', form=form)

@admin.route("job/edit/<int:job_id>", methods=["GET", "POST"])
@admin_required
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    form.update_companylist()
    if form.validate_on_submit():
        form.update_job(job)
        flash('User update success', 'success')
        return redirect(url_for('admin.joblist'))
    return render_template('admin/edit_job.html', form=form, job=job)

@admin.route("job/change_jobstatus/<int:job_id>")
@admin_required
def change_jobstatus(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_online = not job.is_online
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('admin.joblist'))

@admin.route("job/delete/<int:job_id>")
@admin_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('admin.joblist'))
