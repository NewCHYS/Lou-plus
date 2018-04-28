from flask import request
from flask import current_app
from flask import Blueprint, render_template
from flask_login import current_user
from flask import flash

from jobplus.models import db, Job, Jobseeker

job = Blueprint("job", __name__, url_prefix="/job")


@job.route("/")
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.filter_by(online=True).paginate(
        page=page,
        per_page=current_app.config['INDEX_PER_PAGE'],
        error_out=False
    )
    return render_template("job/index.html", pagination=pagination)

@job.route("/<int:job_id>")
def detail(job_id):
    job = Job.query.filter_by(id=job_id, online=True).first_or_404()
    return render_template("job/detail.html", job=job)

@job.route("/<int:job_id>/apply")
def apply(job_id):
    jobseeker = Jobseeker.query.filter_by(user_id=current_user.id).first()
    job = Job.query.filter_by(id=job_id).first()
    if jobseeker in job.jobseeker:
        flash("Resume has already send", "success")
    else:
        jobseeker.job.append(job)
        db.session.add(jobseeker)
        db.session.commit()
        flash("Resume send success", "success")
    return render_template("job/detail.html", job=job)
