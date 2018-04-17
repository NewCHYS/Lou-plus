import re
import redis
import json

from flask import flash
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, IntegerField
from wtforms.validators import Length, Email, EqualTo, Required, URL, NumberRange

from simpledu.models import db, User, Course, Live


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Repeat Password', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

    def validate_username(self, field):
        n = re.search('[^A-Za-z0-9]', field.data)
        if n:
            flash('Username not correct, only use letter and number')
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError('Username exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email exists')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if field.data and not User.query.filter_by(username=field.data).first():
            raise ValidationError('Username not registed')

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Password Error')


class CourseForm(FlaskForm):
    name = StringField('Course name', validators=[Required(), Length(5, 32)])
    description = TextAreaField('Course content', validators=[Required(), Length(20, 256)])
    image_url = StringField('Page picture', validators=[Required(), URL()])
    author_id = IntegerField('Author ID', validators=[Required(), NumberRange(min=1, message='Invalid UserID')])
    submit = SubmitField('Submit')

    def validate_author_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('Author not exist')

    def create_course(self):
        course = Course()
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course

    def update_course(self, course):
        self.populate_obj(course)
        db.session.add(course)
        db.session.commit()
        return course


class UserForm(FlaskForm):
    username = StringField('User name', validators=[Required(), Length(3, 24)])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    role = IntegerField('Role', validators=[Required()])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        n = re.search('[^A-Za-z0-9]', field.data)
        if n:
            flash('Username not correct, only use letter and number')
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError('Username exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email exists')

    def validate_role(self, field):
        if field.data not in [10, 20, 30]:
            raise ValidationError('Invalid role')

    def create_user(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class LiveForm(FlaskForm):
    name = StringField('Live name', validators=[Required(), Length(6, 128)])
    user_id = IntegerField('User ID', validators=[Required(), NumberRange(min=1, message='Invalid UserID')])
    submit = SubmitField('Submit')

    def validate_user_id(self, field):
        if not User.query.get(field.data):
            raise ValidationError('User not exist')

    def create_live(self):
        live = Live()
        self.populate_obj(live)
        db.session.add(live)
        db.session.commit()
        return live

redis = redis.from_url('redis://127.0.0.1:6379')

class SendmessageForm(FlaskForm):
    message = StringField('Message', validators=[Required()])
    submit = SubmitField('Submit')


    def sendmessage(self):
        text = self.message.data
        message = {'username':'System: ', 'text':text}
        redis.publish('chat', json.dumps(message))
