from flask import flash
from flask import redirect, url_for
from flask import current_app, request
from flask import Blueprint, render_template

from jobplus.decorators import admin_required
from jobplus.models import db, User, Company, Jobseeker, Job
from jobplus.forms import UserForm, JobseekerForm, JobForm


admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.route("/")
def index():
    return render_template("admin/index.html")

@admin.route("/userlist")
#@admin_required
def userlist():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/userlist.html', pagination=pagination)
