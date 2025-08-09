from flask import Blueprint, render_template, redirect, url_for
from app.models import Group, User
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage con statistiche generali"""
    total_groups = Group.query.count()
    total_users = User.query.count()
    recent_groups = Group.query.order_by(Group.created_at.desc()).limit(5).all()

    return render_template('index.html',
                           total_groups=total_groups,
                           total_users=total_users,
                           recent_groups=recent_groups)

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard con panoramica completa"""
    return redirect(url_for('main.index'))