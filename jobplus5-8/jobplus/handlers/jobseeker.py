from flask import flash
from flask import request
from flask import current_app
from flask import redirect, url_for
from flask import Blueprint, render_template
from flask_login import current_user

from jobplus.models import db, User, Jobseeker, Job, resumes
from jobplus.forms import JobseekerForm

jobseeker = Blueprint("jobseeker", __name__, url_prefix="/jobseeker")


@jobseeker.route("/")
def index():
    jobseeker_id = current_user.jobseeker.id
    jobseeker = Jobseeker.query.filter_by(id=jobseeker_id).first()
    return render_template('jobseeker/index.html', jobseeker=jobseeker)

@jobseeker.route("/resumesends")
def resume_sends():
    jobseeker_id = current_user.jobseeker.id
    jobseeker = Jobseeker.query.filter_by(id=jobseeker_id).first()
    page = request.args.get('page', default=1, type=int)
    print(type(jobseeker.job))
    pagination = jobseeker.job.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('jobseeker/sends.html', pagination=pagination, jobseeker=jobseeker)

@jobseeker.route("/cancel/<int:job_id>")
def cancel(job_id):
    jobseeker_id = current_user.jobseeker.id
    jobseeker = Jobseeker.query.filter_by(id=jobseeker_id).first()
    job = Job.query.filter_by(id=job_id).first()
    jobseeker.job.remove(job)
    db.session.add(jobseeker)
    db.session.commit()
    flash('Cancel success', 'success')
    return redirect(url_for('jobseeker.resume_sends'))
