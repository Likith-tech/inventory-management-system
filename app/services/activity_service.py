from app import db
from app.models import ActivityLog


def log_activity(user_id, action, entity_type, entity_id=None, description=None):
    entry = ActivityLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        description=description,
    )
    db.session.add(entry)
    return entry
