from flask import Blueprint, request, make_response
from flask.ext.login import login_required, login_user, logout_user, \
    current_user
from runnershigh.user.models import Users
from runnershigh import db, bcrypt, login_manager


mod = Blueprint('auth', __name__)


@login_manager.user_loader
def user_loader(username):
    return Users.query.filter_by(username=username).first()

@mod.route('/register/', methods=['POST'])
def register():
    roles_id = int(request.form.get('roles_id') or None)
    username = request.form.get('username') or None
    email = request.form.get('email') or None
    password = request.form.get('password') or None
    age = request.form.get('age') or None
    location = request.form.get('location') or None

    form_data = [username, email, password, location, roles_id, age]

    if any(x is None for x in form_data):
        resp_msg = "Missing required field"
        return make_response(resp_msg, 400)

    try:
        create_user = Users(
            roles_id = roles_id,
            username = username,
            email = email,
            password = password,
            location = location
        )
        db.session.add(create_user)
        db.session.commit()
        resp_msg = "Created new user"
        return make_response(resp_msg, 201)
    except Exception:
        resp_msg = "Could not create new user"
        return make_response(resp_msg, 500)

@mod.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username') or None
    email = request.form.get('email') or None
    password = request.form.get('password') or None

    user = Users.query.filter_by(username=username).first()
    hashed_password = user.password
    password = password.encode('utf-8')

    if user:
        if bcrypt.check_password_hash(hashed_password, password):
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            resp_msg = "Logged in user: {0}".format(user.username)
            return make_response(resp_msg, 200)
        else:
            resp_msg = "Incorrect password for user: {0}".format(user.username)
            return make_response(resp_msg, 401)
    else:
        resp_msg = "Could not find user: {0}".format(username)
        return make_response(resp_msg, 404)

@login_required
@mod.route('/logout/', methods=['GET'])
def logout():
    user = current_user
    username = user.username
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    resp_msg = "Logged out user: {0}".format(username)
    return make_response(resp_msg, 200)
