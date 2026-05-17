from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import ChangePasswordForm, ProfileEditForm, ProfileImageForm, UserPreferencesForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/')
@login_required
def profile():
    return render_template('profile/profile.html', title='My Profile')


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile/form.html', title='Edit Profile', form=form)


@profile_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = UserPreferencesForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Preferences updated.', 'success')
        return redirect(url_for('profile.settings'))
    return render_template('profile/form.html', title='Preferences', form=form)


@profile_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Password changed.', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile/form.html', title='Change Password', form=form)


@profile_bp.route('/theme', methods=['POST'])
@login_required
def theme():
    selected = request.form.get('theme')
    if selected in {'light', 'dark', 'system'}:
        current_user.preferred_theme = selected
        db.session.commit()
    return redirect(request.referrer or url_for('dashboard.index'))
