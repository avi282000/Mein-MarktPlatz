from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_place():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    purchase_form = PurchaseItemForm()
    if request.method == "POST":  # Purchasing Items
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f'Successfully Bought {purchased_item_object.name} for ${purchased_item_object.price}!', category='success')
            else:
                flash(f'Insufficient Funds in the Wallet (${ current_user.wallet }) for the Purchase (${ purchased_item_object.price })', category='danger')
        return redirect(url_for("market_place"))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        return render_template("market.html", items=items, purchase_form=purchase_form)


@app.route('/about_author')
def author():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    return render_template('about_author.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    form = RegisterForm()
    if form.validate_on_submit():
        user1 = User(username=form.username.data,
                     email=form.email.data,
                     password=form.password1.data)  # Uses password's setter
        db.session.add(user1)
        db.session.commit()
        login_user(user1)
        flash(f'Account Created Successfully! Glad to have you on board {user1.username}!', category='success')
        return redirect(url_for('market_place'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'Error Encountered! : {err_msg}')
            flash(f'Error Encountered! : {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    form = LoginForm()
    if form.validate_on_submit():
        probable_user = User.query.filter_by(username=form.username.data).first()
        if probable_user and probable_user.check_password_legitimacy(probable_password=form.pw.data):
            login_user(probable_user)
            flash(f'Welcome Back {probable_user.username}!', category='success')
            return redirect(url_for('market_place'))
        else:
            flash('Login Credentials Are Incorrect! Please re-check your Username/Password.', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'Logged Out Successfully!', category='info')
    return redirect(url_for('home_page'))
