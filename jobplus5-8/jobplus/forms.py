import re

from flask import flash
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField
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

    def create_company(self):
        print('start create')
        user = User()
        user.email = self.email.data
        user.password = self.password.data
        user.role = 20
        db.session.add(user)
        db.session.commit()
        print('create user ok')
        user_add = User.query.filter_by(email=self.email.data).first()
        company = Company()
        company.name = self.name.data
        company.user_id = user_add.id
        db.session.add(company)
        db.session.commit()
        print('create company ok')
        return user

    def create_jobseeker(self):
        user = User()
        user.email = self.email.data
        user.password = self.password.data
        user.role = 10
        db.session.add(user)
        db.session.commit()
        user_add = User.query.filter_by(email=self.email.data).first()
        jobseeker = Jobseeker()
        jobseeker.name = self.name.data
        jobseeker.user_id = user_add.id
        db.session.add(jobseeker)
        db.session.commit()
        return user


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
