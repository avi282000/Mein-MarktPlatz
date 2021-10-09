from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm
from market import db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market')
def market_place():
    items = Item.query.all()
    return render_template("market.html", items=items)


@app.route('/about_author')
def author():
    return render_template('about_author.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user1 = User(username=form.username.data,
                     email=form.email.data,
                     pw_hash=form.password1.data)
        db.session.add(user1)
        db.session.commit()
        return redirect(url_for('market_place'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            print(f'Error Encountered! : {err_msg}')
            flash(f'Error Encountered! : {err_msg}', category='danger')

    return render_template('register.html', form=form)
