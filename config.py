from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("default_config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)

db = SQLAlchemy(app)
