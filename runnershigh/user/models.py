import datetime
from revolvr import db, bcrypt


class Roles(db.Model):

    __tablename__ = 'roles'

    roles_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Users(db.Model):

    __tablename__ = 'users'

    users_id = db.Column(db.Integer, primary_key=True)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.roles_id'))
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    age = db.Column(db.Integer)
    location = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    roles = db.relationship('Roles')
    content = db.relationship('Content')
    content_views = db.relationship('ContentViews')

    @property
    def serialize_auth(self):
        return {
            "users_id": self.users_id,
            "username": self.username,
            "email": self.email,
            "location": self.location
        }

    @property
    def serialize_noauth(self):
        return {
            "users_id": self.users_id,
            "username": self.username,
            "location": self.location
        }

    def is_admin(self):
        if self.roles.name == 'admin':
            return True
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.username

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

@db.event.listens_for(Users, 'before_insert')
def encrypt_password(mapper, connect, self):
    self.password = bcrypt.generate_password_hash(self.password.encode('utf-8'))


class Login(db.Model):

    __tablename__ = 'login'

    login_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    last_login_ip = db.Column(db.String)
    last_login = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Banned(db.Model):

    __tablename__ = 'banned'

    banned_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    banned_by_users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    reason = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow())


class Blocked(db.Model):

    __tablename__ = 'blocked'

    blocked_id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
    blocked_users_id = db.Column(db.Integer, db.ForeignKey('users.users_id'))
