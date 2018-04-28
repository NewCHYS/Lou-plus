from flask import flash
from flask import request
from flask import current_app, redirect, url_for
from flask import Blueprint, render_template
from flask_login import current_user

from jobplus.models import db, Company, Job
from jobplus.forms import JobForm

company = Blueprint("company", __name__, url_prefix="/company")


@company.route("/")
def index():
    page = request.args.get('page', default=1, type=int)

    pagination = Company.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template("company/index.html", pagination=pagination)

@company.route("/<int:company_id>")
def detail(company_id):
    company = Company.query.filter_by(id=company_id).first()
    return render_template("company/detail.html", company=company)

@company.route("/<int:company_id>/jobs")
def jobs(company_id):
    company = Company.query.filter_by(id=company_id).first()
    return render_template("company/detail-job.html", company=company)

@company.route("/admin")
def admin_index():
    company = Company.query.filter_by(id=current_user.company.id).first()
    return render_template("company/admin/index.html", company=company)

@company.route("/admin/jobs")
def admin_jobs():
    company_id = current_user.company.id
    company = Company.query.filter_by(id=company_id).first()
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(company_id=company_id).paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template("company/admin/jobs.html", pagination=pagination, company=company)


@company.route("/job_create", methods=["GET", "POST"])
def create_job():
    company_id = current_user.company.id
    form = JobForm()
    form.update_companylist()
    form.company_id.data = company_id
    if form.validate_on_submit():
        form.create_job()
        flash('Job create success', 'success')
        return redirect(url_for('company.admin_jobs'))
    return render_template('company/admin/add_job.html', form=form)

@company.route("/job/edit/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    form.update_companylist()
    if form.validate_on_submit():
        form.update_job(job)
        flash('Job update success', 'success')
        return redirect(url_for('company.admin_jobs'))
    return render_template('company/admin/edit_job.html', form=form, job_id=job_id)

@company.route("/change_userstatus/<int:job_id>")
def change_jobstatus(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_online = not job.is_online
    db.session.add(job)
    db.session.commit()
    return redirect(url_for('company.admin_jobs'))

@company.route("/delete/<int:job_id>")
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    flash('Job delete success', 'success')
    return redirect(url_for('company.admin_jobs'))
