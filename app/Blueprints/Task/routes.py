from flask import Blueprint

taskBlueprint = Blueprint('taskBlueprint', __name__,
                          template_folder='pages', static_folder='static')
