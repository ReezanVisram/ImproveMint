from flask import Blueprint

userBlueprint = Blueprint('userBlueprint', __name__,
                          template_folder='pages', static_folder='static')
