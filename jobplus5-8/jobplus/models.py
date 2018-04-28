from datetime import datetime
from flask import url_for
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(Base, UserMixin):
    __tablename__ = "user"

    ROLE_JOBSEEKER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True, nullable=False)
    _password = db.Column("password", db.String(256), nullable=False)
    role = db.Column(db.SmallInteger, default=ROLE_JOBSEEKER)

    enabled = db.Column(db.Boolean, default=True)

    company = db.relationship("Company", cascade="all,delete", back_populates="user", uselist=False)
    jobseeker = db.relationship("Jobseeker", cascade="all,delete", back_populates="user", uselist=False)

    def __reper__(self):
        return "<User:{}>".format(self.usernmae)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_jobseeker(self):
        return self.role == self.ROLE_JOBSEEKER

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

    @property
    def is_enabled(self):
        return self.enabled

    @is_enabled.setter
    def is_enabled(self, status):
        self.enabled = status


class Company(Base):
    __tablename__ = "company"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True, nullable=False)
    location = db.Column(db.String(128))
    short_description = db.Column(db.String(128))
    description = db.Column(db.String(512))
    image_url = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="company")

    job = db.relationship("Job", cascade="all,delete", back_populates="company")

    def __repr__(self):
        return "<Company:{}>".format(self.name)

    @property
    def url(self):
        return url_for("company.detail", company_id=self.id)

    @property
    def jobnumber(self):
        return len(self.job)


resumes = db.Table(
    "resumes",
    db.Column("jobseeker_id", db.Integer, db.ForeignKey("jobseeker.id")),
    db.Column("job_id", db.Integer, db.ForeignKey("job.id")),
)


class Jobseeker(Base):
    __tablename__ = "jobseeker"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(20))
    resume = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    user = db.relationship("User", back_populates="jobseeker")

    job = db.relationship(
        "Job", secondary=resumes, backref=db.backref("jobseeker", lazy="dynamic"), lazy="dynamic"
    )

    def __repr__(self):
        return "<Jobseeker:{}>".format(self.name)

    @property
    def url(self):
        return url_for("jobseeker.detail", jobseeker_id=self.id)


class Job(Base):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    salary = db.Column(db.String(128))
    experience = db.Column(db.String(128))
    location = db.Column(db.String(128))
    description = db.Column(db.String(512))
    requirement = db.Column(db.String(512))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))

    online = db.Column(db.Boolean, default=True)

    company = db.relationship("Company", back_populates="job", uselist=False)

    @property
    def is_online(self):
        return self.online

    @is_online.setter
    def is_online(self, status):
        self.online = status

#    jobseeker = db.relationship(
#        "Jobseeker", secondary=resumes, backref=db.backref("job", cascade='all,delete', lazy="dynamic")
#    )
