from flask import Blueprint

habitBlueprint = Blueprint('habitBlueprint', __name__,
                           template_folder='pages', static_folder='static')
