from datetime import datetime

from app import db


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(80), nullable=False)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    file_path = db.Column(db.String(255))
    generated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User')
