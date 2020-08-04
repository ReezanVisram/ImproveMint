from flask import Blueprint

dashboardBlueprint = Blueprint('dashboardBlueprint', __name__, template_folder='pages', static_folder='static')

@dashboardBlueprint.route('/')
def dashboardHomeRoute():
    currUser = User.query.filter_by(id=session['userId']).first()
    return render_template('dashboard.html', name=currUser.username)