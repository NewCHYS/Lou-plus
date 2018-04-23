from flask import request
from flask import current_app
from flask import Blueprint, render_template

from jobplus.models import Company

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
    print("Company id:{}".format(company_id))
    return render_template("company/detail.html")

@company.route("/<int:company_id>/jobs")
def jobs(company_id):
    return render_template("company/detail.html")

