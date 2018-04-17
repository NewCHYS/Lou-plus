import json

from flask import Blueprint, render_template
from flask import flash
from flask import redirect, url_for

from simpledu.decorators import admin_required
from simpledu.models import Live


live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
    live = Live.query.order_by(Live.id.desc()).first()
    if live:
        return render_template('live/index.html', live=live)
    else:
        return render_template('live/index.html')

