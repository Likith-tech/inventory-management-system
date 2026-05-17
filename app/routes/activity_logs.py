from flask import Blueprint, render_template
from flask_login import login_required

from app.models import ActivityLog
from app.utils.permissions import roles_required

bp = Blueprint('activity_logs', __name__, url_prefix='/activity-logs')


@bp.route('/')
@login_required
@roles_required('admin', 'manager')
def list_logs():
    logs = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(100).all()
    return render_template('activity_logs/list.html', title='Activity Logs', logs=logs)
