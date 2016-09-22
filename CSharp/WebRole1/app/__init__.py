from flask import Flask
from flask_mongoengine import MongoEngine
from app import config

app = Flask(__name__)
app.config.from_object(config)

db = MongoEngine(app)

from app import views