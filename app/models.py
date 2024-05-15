from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone

class ShareLink(db.Model):
    __tablename__ = 'sharelink'
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    depth: so.Mapped[int]
    gas: so.Mapped[int]
    solve: so.Mapped[int]
    hash: so.Mapped[str] = so.mapped_column(sa.String(6), index=True,
                                             unique=True)
    created: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: sa.func.now())


'''
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' %self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' %self.username
'''
'''
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Divespot(db.Model):
    __tablename__ = 'divespots'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    depth = db.Column(db.Integer)
    type = db.Column(db.String(30))
    posLat = db.Column(db.String(30))
    posLng = db.Column(db.String(30))
    images = db.relationship('Image', backref='divespot', lazy='dynamic')


    def __repr__(self):
        return '<Divespot %r>' %self.name

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    divespotID = db.Column(db.Integer, db.ForeignKey('divespots.id'))

    def __repr__(self):
        return '<Image %r>' %self.image
'''