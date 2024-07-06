from flask import Flask, render_template, request, redirect, url_for, flash, make_response, blueprints, jsonify, Response, send_file, g, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import SelectField
from flask_cors import CORS
from flask_migrate import Migrate
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import mysql.connector as mysql
from mysql.connector import Error
import sqlite3 as sql
import database
import os
import random
from dotenv import load_dotenv
import secrets
import redis

load_dotenv()

app = Flask(__name__)
CORS(app)
token = secrets.token_hex(64)
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
app.secret_key = token
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(redis_url)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = False
app.config['FLASK_ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['FLASK_APP'] = 'app.py'

server_session = Session(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            print("User is logged in")
            return f(*args, **kwargs)
        else:
            flash("You need to login for access")
            return redirect(url_for('login'))
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_superuser' in session and session['is_superuser']:
            print("User is admin")
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin to access this page")
            return redirect(url_for('login'))
    return wrap


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


headers = {
    'Content-Type': 'text/html',
    'charset': 'utf-8',
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With",
    "Authorization": "Bearer " + token
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index-2')
def index_2():
    return render_template('index-2.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('sign-up.html')

@app.route('/all_food')
def all_food():
    return render_template('all-food.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

# create a route for terms-service, trust-safety, privacy-policy, food-details, blog, blog-details, logout, shopping-cart, shopping-cart-02, shopping-cart-address, shopping-cart-new-address
@app.route('/terms-service')
def terms_service():
    return render_template('terms-service.html')

@app.route('/trust-safety')
def trust_safety():
    return render_template('trust-safety.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/foods-details')
def foods_details():
    return render_template('foods-details.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog-details')
def blog_details():
    return render_template('blog-details.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/shopping-cart')
def shopping_cart():
    return render_template('shopping-cart.html')

@app.route('/shopping-cart-02')
def shopping_cart_02():
    return render_template('shopping-cart-02.html')

@app.route('/shopping-cart-address')
def shopping_cart_address():
    return render_template('shopping-cart-address.html')

@app.route('/shopping-cart-new-address')
def shopping_cart_new_address():
    return render_template('shopping-cart-new-address.html')




if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')