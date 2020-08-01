from flask import Flask
from app.Models import db

app = Flask(__name__)
db.init_app(app)


if (app['ENV'] == 'production'):
    app.config.from_object('config.ProductionConfig')

elif (app['ENV'] == 'testing'):
    app.config.from_object('config.TestingConfig')

else:
    app.config.from_object('config.DevelopmentConfig')