import os
import config
from flask import Blueprint, request, make_response, jsonify
from flask.ext.login import login_required, login_user, logout_user, \
    current_user
from runnershigh import db, server, bcrypt
from runnershigh.user.models import Users


mod = Blueprint('user', __name__)


@login_required
@mod.route('/users/<username>/', methods=['GET', 'PUT', 'DELETE'])
def users(username=None):

    if request.method == 'PUT':
        user = Users.query.filter_by(username=username).first()
        if user.username == current_user.username and user.is_authenticated() or user.is_admin():
            username = request.form.get('username') or None
            email = request.form.get('email') or None
            password = request.form.get('password') or None
            age = request.form.get('age') or None
            location = request.form.get('location') or None
            try:
                login_user(user)
                user.username = username
                user.email = email
                user.password = bcrypt.generate_password_hash \
                    (password.encode('utf-8'))
                user.age = age
                user.location = location
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                resp_msg = "Updated user"
                return make_response(resp_msg, 200)
            except Exception:
                resp_msg = "Could not update user"
                return make_response(resp_msg, 500)
        else:
            resp_msg = "Not authorized to update user"
            return make_response(resp_msg, 401)

    if request.method == 'GET':
        user = Users.query.filter_by(username=username).first()
        if user.is_authenticated():
            if user.username == current_user.username:
                resp_msg = jsonify(user.serialize_auth)
                return make_response(resp_msg, 200)
            else:
                resp_msg = jsonify(user.serialize_noauth)
                return make_response(resp_msg, 200)
        else:
            resp_msg = "Users must be authenticated to view content"
            return make_response(resp_msg, 403)

    if request.method == 'DELETE':
        user = Users.query.filter_by(username=username).first()
        if user.username == current_user.username and user.is_authenticated() or user.is_admin():
            Users.query.filter_by(users_id=user.users_id).delete()
            db.session.commit()
            resp_msg = "Deleted user"
            return make_response(resp_msg, 200)
        resp_msg = "Not authorized to delete user"
        return make_response(resp_msg, 401)
