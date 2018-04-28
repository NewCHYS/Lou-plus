from flask import abort
from flask import current_app
from flask_login import current_user
from functools import wraps

from jobplus.models import User


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwrargs):
            if role==User.ROLE_ADMIN and current_app.config['ADMIN_REQUIRED']:
                if not current_user.is_authenticated:
                    return current_app.login_manager.unauthorized()
                if not current_user.is_admin:
                    abort(404)
            elif role==User.ROLE_COMPANY and currnet_app.config['COMPANY_REQUIRED']:
                if not current_user.is_authenticated:
                    return current_app.login_manager.unauthorized()
                if not current_user.is_company:
                    abort(404)
            else:
                return func(*args, **kwrargs)
            return func(*args, **kwrargs)
        return wrapper
    return decorator

company_required = role_required(User.ROLE_COMPANY)
admin_required = role_required(User.ROLE_ADMIN)
