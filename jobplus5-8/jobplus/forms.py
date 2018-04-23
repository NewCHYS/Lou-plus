import re

from flask import flash
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField
)
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange

from jobplus.models import db, User, Company, Jobseeker, Job


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(3, 30)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Repeat Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email exists')

    def create_user(self, role):
        print('start create')
        user = User()
        user.email = self.email.data
        user.password = self.password.data
        user.role = role
        db.session.add(user)
        db.session.commit()
        user_add = User.query.filter_by(email=self.email.data).first()
        if role == 20:
            company = Company()
            company.name = self.name.data
            company.user_id = user_add.id
            db.session.add(company)
            db.session.commit()
        elif role == 10:
            jobseeker = Jobseeker()
            jobseeker.name = self.name.data
            jobseeker.user_id = user_add.id
            db.session.add(jobseeker)
        print('create user ok')


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Required(), Email()])
    password = PasswordField("Password", validators=[Required(), Length(6, 24)])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Submit")

    def validate_email(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if not user:
            raise ValidationError("Email not registed")

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError("Password Error")


class UserForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(3, 30)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
#    role = StringField('Role', validators=[Required()])
    role = SelectField('Job', coerce=int, choices=[
        (10, 'Jobsekker'),
        (20, 'Company')
    ])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email exists')

    def create_user(self):
        print('start create')
        user = User()
        user.email = self.email.data
        user.password = self.password.data
        user.role = self.role.data
        db.session.add(user)
        db.session.commit()
        print('create user ok')
        user_add = User.query.filter_by(email=self.email.data).first()
        if user.role == 10:
            jobseeker = Jobseeker()
            jobseeker.name = self.name.data
            jobseeker.user_id = user_add.id
            db.session.add(jobseeker)
        elif user.role == 20:
            company = Company()
            company.name = self.name.data
            company.user_id = user_add.id
            db.session.add(company)
        db.session.commit()
        print('create ok')

    def update_user(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        print('update user ok')
        if user.role == 10:
            jobseeker = Jobseeker.query.filter_by(user_id=user.id).first()
            jobseeker.name = self.name.data
            db.session.add(jobseeker)
        elif user.role == 20:
            company = Company.query.filter_by(user_id=user.id).first()
            company.name = self.name.data
            db.session.add(company)
        db.session.commit()
        print('update ok')


class CompanyForm(FlaskForm):

    def update_company(self):
        pass


class JobseekerForm(FlaskForm):

    def update_jobseeker(self):
        pass


class JobForm(FlaskForm):
    name = StringField('Name', validators=[Required(), Length(3, 30)])
    company_id = SelectField('Job', coerce=int, choices=[])
    submit = SubmitField('Submit')


    def update_companylist(self):
        companylist = []
        c = Company.query.all()
        for item in c:
            companylist.append((item.id, item.name))
        self.company_id.choices = companylist

    def create_job(self):
        job = Job()
        job.name = self.name.data
        job.company_id = self.company_id.data
        db.session.add(job)
        db.session.commit()

    def update_job(self, job):
        job.name = self.name.data
        job.company_id = self.company_id.data
        db.session.add(job)
        db.session.commit()


class ResumeForm(FlaskForm):

    def create_resume(self):
        pass

    def update_resume(self):
        pass

