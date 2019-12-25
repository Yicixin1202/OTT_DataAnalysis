from flask import Blueprint

app_file = Blueprint("app_file", __name__)

from .views import *
