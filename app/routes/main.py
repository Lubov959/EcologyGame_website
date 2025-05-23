from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def show():
    return render_template('main/index.html')

