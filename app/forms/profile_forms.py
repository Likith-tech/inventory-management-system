from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    bio = TextAreaField('Bio')
    submit = SubmitField('Save Profile')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class ProfileImageForm(FlaskForm):
    profile_image = FileField('Profile Image')
    submit = SubmitField('Upload')


class UserPreferencesForm(FlaskForm):
    preferred_theme = SelectField('Theme', choices=[('light', 'Light'), ('dark', 'Dark'), ('system', 'System')])
    dashboard_density = SelectField('Dashboard Density', choices=[('comfortable', 'Comfortable'), ('compact', 'Compact')])
    email_notifications = BooleanField('Email Notifications')
    submit = SubmitField('Save Preferences')
