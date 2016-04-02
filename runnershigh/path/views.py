from flask import Blueprint, request, make_response
from flask.ext.login import login_required, current_user


mod = Blueprint('path', __name__)
