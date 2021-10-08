from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SECRET_KEY'] = 'c72c6dc55741ce3e40667084'

db = SQLAlchemy(app)

from market import routes

