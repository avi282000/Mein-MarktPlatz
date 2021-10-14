from market import db
from market import bcrypt
from market import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email = db.Column(db.String(length=40), nullable=False, unique=True)
    pw_hash = db.Column(db.String(length=60), nullable=False)
    wallet = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_by', lazy=True)

    @property
    def nice_looking_wallet(self):
        if len(str(self.wallet)) >= 4:
            return f'${str(self.wallet)[:-3]},{str(self.wallet)[-3:]}'
        else:
            return f"${self.wallet}"

    @property
    def password(self): # Returns the password
        return self.password

    @password.setter
    def password(self, plain_text_password):  # Used for generating pw_hash
        self.pw_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_legitimacy(self, probable_password):
        return bcrypt.check_password_hash(self.pw_hash, probable_password)

    def can_purchase(self, item_object):
        return self.wallet >= item_object.price

    def can_sell(self, item_object):
        return item_object in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'{self.name}'

    def buy(self, user):
        self.owner = user.id
        user.wallet -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.wallet += self.price
        db.session.commit()
