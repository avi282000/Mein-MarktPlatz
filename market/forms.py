from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check): # It's a syntax for naming a validation function. Raw terms: def validate_FIELDNAME(self, arg)
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try another!")

    def validate_email(self, email_to_check): # It's a syntax for naming a validation function. Raw terms: def validate_FIELDNAME(self, arg)
        email_address = User.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError("An account with the same Email Address is already registered. Forgot your password?")

    username = StringField(label='User Name:', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create The Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    pw = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Yes. Purchase the Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell the Item!')