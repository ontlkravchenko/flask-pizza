import os
from flask import Flask, render_template, request, redirect, session, flash, g, url_for
from flask_session import Session
import sqlite3
import re
from werkzeug.security import generate_password_hash, check_password_hash
import string
import random

# Adding session secret key
application = Flask(__name__)
application.secret_key = b'd0a00f2e8c66f15125d81bf4a558a2152bef2eca0d68b7df0da9470da77c4c9d'

# Const variables
MAX_PRODUCT = 10
PRODUCTS_LIST = ["Pizza cyber paperoni", "Pizza cyber police", "Default pizza", "Happy Friday Pizza",
                 "Cyber Vegan", "Future", "Noname-pizza", "Ukrainian pizza", "CS50 pizza", "Last pizza"]
MAX_SIZE = 3
PRODUCTS_SIZE = ["Standard", "Big", "Large", "Huge"]
MAX_THICKNESS = 1
PRODUCTS_THICK = ["Thin", "Thick"]
MAX_TOPPINGS = 1
PRODUCTS_TOP = ["Without", "Onions"]

"""Connecting DB"""
DATABASE = './pizza.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    db.row_factory = make_dicts
    return db


@application.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Hash for cart id generator


def cart_hash_gen():
    hash_digits = string.digits
    hash_punctuation = string.punctuation
    hash_letters = string.ascii_letters
    st = ''

    for i in range(10):
        st += random.choice(hash_digits)
        st += random.choice(hash_punctuation)
        st += random.choice(hash_letters)
    return st

# Implementing routes


@application.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    name = request.form.get('name')
    email = request.form.get('email')
    password = str(request.form.get('pass'))
    password = generate_password_hash(password)
    regex = r"^[a-zA-Z0-9\_]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+"

    # Checking if user already exists
    namedb = query_db(
        "SELECT name FROM users WHERE email = ? OR email = ?", (email, email))

    if namedb != []:
        flash("e-mail already taken")
        return redirect(url_for('signup'))

    # Making SQL query for registration
    if request.method == 'POST':
        # Validating data
        if name.isalpha() == False:
            flash("Please provide valid name")
            return redirect(url_for('signup'))
        elif not re.match(regex, email):
            flash("Please provide valid e-mail")
            return redirect(url_for('signup'))
        elif len(password) < 4:
            flash("Your password must be minimum 4 characters")
            return redirect(url_for('signup'))
        # TODO: if user is already in db

        query_db("INSERT INTO users (name, email, pass) VALUES (?, ?, ?)",
                 (name, email, password))
        get_db().commit()

        return redirect('/')

    return render_template('signup.html', error=error)


@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        error = None
        email = request.form.get('email')
        password = str(request.form.get('pass'))
        regex = r"^[a-zA-Z0-9\_]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+"

        # Validate inputs
        if not re.match(regex, email):
            flash("Please provide valid e-mail")
            return redirect('/')
        elif len(password) < 4:
            flash("Your password must be minimum 4 characters")
            return redirect('/')

        # Comparing to data from db
        namedb = query_db(
            "SELECT name FROM users WHERE email = ? OR email = ?", (email, email))
        passdb = query_db(
            "SELECT pass FROM users WHERE email = ? OR email = ?", (email, email))
        get_db().commit()

        if namedb == []:
            flash("Wrong e-mail")
        elif check_password_hash(passdb[0]['pass'], password) == False:
            flash("Wrong password")
        else:
            session['email'] = email
            session['name'] = namedb[0]['name']
            return redirect(url_for('order'))

    return render_template('index.html')


@application.route('/order', methods=['GET', 'POST'])
def order():
    if not 'email' in session:
        return redirect('/')
    # Inserting user id into session
    usr_id = query_db("SELECT id FROM users WHERE email = ? OR name = ?",
                      (session['email'], session['email']))
    session['user_id'] = int(usr_id[0]['id'])
    get_db().commit()

    if request.method == 'POST':
        product = int(request.form.get('product'))
        size = int(request.form.get('size'))
        thickness = int(request.form.get('thickness'))
        toppings = int(request.form.get('toppings'))

        # Validating data
        if product > MAX_PRODUCT or product < 0:
            return redirect(url_for('forhackers'))
        if size > 3 or MAX_SIZE < 0:
            return redirect(url_for('forhackers'))
        if thickness > MAX_THICKNESS or thickness < 0:
            return redirect(url_for('forhackers'))
        if toppings > MAX_TOPPINGS or toppings < 0:
            return redirect(url_for('forhackers'))

        # Checking if hash is already exists in db (almosg impossible, but still)
        carts_ids_from_db = query_db("SELECT cart_id FROM cart")
        # get_db().commit()

        if not 'cart_hash' in session or session['cart_hash'] == None:
            cart_id_hash = cart_hash_gen()
            for i in range(len(carts_ids_from_db)):
                if i == len(carts_ids_from_db):
                    break
                else:
                    if cart_id_hash == carts_ids_from_db[i]['cart_id']:
                        cart_id_hash = cart_hash_gen()
                        i = 0
            session['cart_hash'] = cart_id_hash

        # Inserting info about pizza
        query_db("INSERT INTO cart (name_id, size, thickness, toppings, cart_id) VALUES (?, ?, ?, ?, ?)",
                 (product, size, thickness, toppings, session['cart_hash']))
        get_db().commit()

    return render_template('order.html', products=PRODUCTS_LIST, sizes=PRODUCTS_SIZE, lsize=len(PRODUCTS_SIZE),
                           thick=PRODUCTS_THICK, lthick=len(PRODUCTS_THICK),
                           top=PRODUCTS_TOP, ltop=len(PRODUCTS_TOP))


@application.route('/cart', methods=['GET', 'POST'])
def cart():
    if not 'email' in session:
        return redirect('/')

    if session['cart_hash'] == None:
        return render_template('cart-empty.html')

    # Getting list of all products
    cart_history = query_db("SELECT * from cart WHERE cart_id = ? OR cart_id = ?",
                            (session['cart_hash'], session['cart_hash']))
    if cart_history == []:
        return render_template('cart-empty.html')

    return render_template('cart.html', history=cart_history, hlen=len(cart_history), products=PRODUCTS_LIST,
                           sizes=PRODUCTS_SIZE, thick=PRODUCTS_THICK, top=PRODUCTS_TOP)


@application.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Getting list of all products
    cart_history = query_db("SELECT * from cart WHERE cart_id = ? OR cart_id = ?",
                            (session['cart_hash'], session['cart_hash']))

    removed_id = int(request.form.get('row'))
    query_db("DELETE FROM cart WHERE id = ? AND id = ?",
             (cart_history[removed_id]['id'], cart_history[removed_id]['id']))
    get_db().commit()
    return redirect(url_for('cart'))


@application.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('cart_hash', None)
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect('/')


@application.route('/forhackers')
def forhackers():
    return "<h1>Do not try to hack my web site, please :)</h1>"


if __name__ == '__main__':
    application.run(debug=True)
