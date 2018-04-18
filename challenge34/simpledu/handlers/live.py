import json

from flask import Blueprint, render_template
from flask import flash
from flask import redirect, url_for

from simpledu.decorators import admin_required
from simpledu.models import Live
from simpledu.forms import MessageForm
from .ws import redis 


live = Blueprint('live', __name__, url_prefix='/live')

@live.route('/')
def index():
    live = Live.query.order_by(Live.id.desc()).first()
    if live:
        return render_template('live/index.html', live=live)
    else:
        return render_template('live/index.html')

@live.route('/systemmessage', methods=['GET', 'POST'])
@admin_required
def systemmessage():
    form = MessageForm()
    if form.validate_on_submit():
        message = {'username':'System', 'text':form.message.data}
        redis.publish('chat', json.dumps(message))
        flash('System message send success', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/message.html', form=form)
