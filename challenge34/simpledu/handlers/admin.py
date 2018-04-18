from flask import flash
from flask import redirect, url_for
from flask import render_template, current_app, request
from flask import Blueprint

from simpledu.decorators import admin_required
from simpledu.models import db, User, Course, Live
from simpledu.forms import UserForm, CourseForm, LiveForm


admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin.route('/courses')
@admin_required
def courses():
    page = request.args.get('page', default=1, type=int)
    pagination = Course.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/courses.html', pagination=pagination)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        form.create_course()
        flash('Course create success', 'success')
        return redirect(url_for('admin.course'))
    return render_template('admin/create_course.html', form=form)

@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)
    if form.validate_on_submit():
        form.update_course(course)
        flash('Course update success', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/edit_course.html', form=form, course=course)

@admin.route('/courses/<int:course_id>/delete')
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Course delete success', 'success')
    return redirect(url_for('admin.courses'))

@admin.route('/user')
@admin_required
def user():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/user.html', pagination=pagination)

@admin.route('/user/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        form.create_user()
        flash('User create success', 'success')
        return redirect(url_for('admin.user'))
    return render_template('admin/create_user.html', form=form)

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.update_user(user)
        flash('User update success', 'success')
        return redirect(url_for('admin.user'))
    return render_template('admin/edit_user.html', form=form, user=user)

@admin.route('/user/<int:user_id>/delete')
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User delete success', 'success')
    return redirect(url_for('admin.user'))

@admin.route('/live')
@admin_required
def live():
    page = request.args.get('page', default=1, type=int)
    pagination = Live.query.paginate(
        page=page,
        per_page=current_app.config['ADMIN_PER_PAGE'],
        error_out=False
    )
    return render_template('admin/live.html', pagination=pagination)

@admin.route('/live/create', methods=['GET', 'POST'])
@admin_required
def create_live():
    form = LiveForm()
    if form.validate_on_submit():
        form.create_live()
        flash('Live create success', 'success')
        return redirect(url_for('admin.live'))
    return render_template('admin/create_live.html', form=form)

@admin.route('/message', methods=['GET', 'POST'])
@admin_required
def message():
    return redirect(url_for('live.systemmessage'))

