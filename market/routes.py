from market import app
from flask import render_template, redirect, url_for, flash, request,jsonify
from market.models import Item, User, items_share_schema
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    return render_template('home.html')


@app.route('/admin0x47e5534e3abd569c03c0e593b904b4266069feb8bbd0e8aeed8b5e30e277Controls')
def admin_controls():
    items = Item.query.filter_by()
    users = User.query.filter_by()
    return render_template('admin_controls.html', items=items, users=users)


@app.route('/0x256b3bafe9c099dcffb7b40c76f3571007', methods=['GET'])
def db_page():
    shares = db.session.query(Item).all()
    result = items_share_schema.dump(shares)
    return jsonify(result)

#    items = []
#    for item in Item.query.all():
#        items.append(item.id)
#        items.append(item.name)
#        items.append(item.price)
#        items.append(item.barcode)
#        items.append(item.description)
#    return jsonify([items])


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_place():
    flash(f'ACHTUNG! This Site Is Under Construction!', category='info')
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == "POST":
        # Purchasing Items
        purchased_item = request.form.get('purchased_item')
        purchased_item_object = Item.query.filter_by(name=purchased_item).first()
        if purchased_item_object:
            if current_user.can_purchase(purchased_item_object):
                purchased_item_object.buy(current_user)
                flash(f'Successfully Bought {purchased_item_object.name} for ${purchased_item_object.price}!', category='success')
            else:
                flash(f'Insufficient Funds in the Wallet (${ current_user.wallet }) for the Purchase (${ purchased_item_object.price })', category='danger')

        # Selling Items
        sold_item = request.form.get('sold_item')
        sold_item_object = Item.query.filter_by(name=sold_item).first()
        if sold_item_object:
            if current_user.can_sell(sold_item_object):
                sold_item_object.sell(current_user)
                flash(f'{sold_item_object.name} has been successfully put back on the shelf. You\'ve gained ${sold_item_object.price}!', category='success')
            else:
                flash(f'Something went wrong :(', category='danger')

        return redirect(url_for("market_place"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)


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
