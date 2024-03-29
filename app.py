#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# =============================================================================#
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'
        ]['client_id']

# =============================================================================#

engine = create_engine('sqlite:///categoriesmenuwithusers.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

# =============================================================================#

DBSession = sessionmaker(bind=engine)
session = DBSession()


###############################################################################

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase
                    + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# =============================================================================#

@app.route('/gconnect', methods=['POST'])
def gconnect():

    # Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'
                                 ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code

    code = request.data

    try:

        # Upgrade the authorization code into a credentials object

        oauth_flow = flow_from_clientsecrets('client_secrets.json',
                scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = \
            make_response(json.dumps('Failed to upgrade the authorization code.'
                          ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    url = \
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' \
        % access_token
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.

    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = \
            make_response(json.dumps("Token's user ID doesn't match given user ID."
                          ), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.

    if result['issued_to'] != CLIENT_ID:
        response = \
            make_response(json.dumps("Token's client ID does not match app's."
                          ), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = \
            make_response(json.dumps('Current user is already connected.'
                          ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info

    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += \
        ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash('you are now logged in as %s' % login_session['username'])
    print 'done!'
    return output


# =============================================================================#

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = \
            make_response(json.dumps('Current user not connected.'),
                          401)
        response.headers['Content-Type'] = 'application/json'
        return response

    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' \
        % access_token

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'
                                 ), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = \
            make_response(json.dumps('Failed to revoke token for given user.'
                          , 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# =============================================================================#

@app.route('/categories/<int:category_id>/<int:item_id>/JSON')
def oneItemJSON(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id, category_id=category_id).one()
    return jsonify([item.serialize])


# =============================================================================#

@app.route('/categories/<int:category_id>/JSON')
def oneCategoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


# =============================================================================#

@app.route('/categories/JSON')
def categoryJSON():
    category = session.query(Category).filter_by().all()
    return jsonify(Category=[c.serialize for c in category])


# =============================================================================#

@app.route('/')
@app.route('/categories/')
def listCategories():
    categories = session.query(Category)
    if 'username' not in login_session:
        return render_template('pub_categor.html',
                               categories=categories)
    else:
        return render_template('categories.html', categories=categories)


# =============================================================================#

@app.route('/categories/new', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        category = Category(name=request.form['name'],
                            user_id=login_session['user_id'])
        if category.name != '':
            session.add(category)
            session.commit()
            flash('new category is added!')
        else:
            flash('Empty is not allowed!')
        return redirect(url_for('listCategories'))
    else:
        return render_template('newCategory.html')


# =============================================================================#

@app.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'
           ])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = \
        session.query(Category).filter_by(id=category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return render_template('alert.html')
    else:
        if request.method == 'POST':
            if request.form['name']:
                editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            flash('Category is edited!')
            return redirect(url_for('listCategories'))
        else:
            return render_template('editCategory.html',
                                   category_id=category_id,
                                   c=editedCategory)


# =============================================================================#

@app.route('/categories/<int:category_id>/delete', methods=['GET',
           'POST'])
def deleteCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    toDeleteCategory = \
        session.query(Category).filter_by(id=category_id).one()
    if toDeleteCategory.user_id != login_session['user_id']:
        return render_template('alert.html')
    else:
        if request.method == 'POST':
            session.delete(toDeleteCategory)
            session.commit()
            flash('Category is deleted!')
            return redirect(url_for('listCategories'))
        else:
            return render_template('deleteCategory.html',
                                   category_id=category_id,
                                   c=toDeleteCategory)


# =============================================================================#

@app.route('/categories/<int:category_id>/')
def listCategory(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id)
    return render_template('category.html', category=category,
                           items=items)


# =============================================================================#

@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if category.user_id != login_session['user_id']:
        return render_template('alert.html')
    else:
        if request.method == 'POST':
            item = Item(name=request.form['name'],
                        category_id=category_id,
                        user_id=login_session['user_id'])
            if item.name != '':
                session.add(item)
                session.commit()
                flash('new item is added!')
            else:
                flash('Empty is not allowed!')
            return redirect(url_for('listCategory',
                            category_id=category_id))
        else:
            return render_template('newItem.html',
                                   category_id=category_id)


# =============================================================================#

@app.route('/categories/<int:category_id>/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    if editedItem.user_id != login_session['user_id']:
        return render_template('item_alert.html')
    else:
        if request.method == 'POST':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['description']:
                editedItem.description = request.form['description']
            if request.form['category']:
                editedItem.category_id = request.form['category']
            session.add(editedItem)
            session.commit()
            flash('item is edited!')
            return redirect(url_for('listCategory',
                            category_id=category_id))
        else:
            return render_template('editItem.html',
                                   category_id=category_id,
                                   item_id=item_id, i=editedItem)


# =============================================================================#

@app.route('/categories/<category_id>/<item_id>/delete', methods=['GET'
           , 'POST'])
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    toDeleteItem = session.query(Item).filter_by(id=item_id).one()
    if toDeleteItem.user_id != login_session['user_id']:
        return render_template('item_alert.html')
    else:
        if request.method == 'POST':
            session.delete(toDeleteItem)
            session.commit()
            flash('item is deleted!')
            return redirect(url_for('listCategory',
                            category_id=category_id))
        else:
            return render_template('deleteItem.html',
                                   category_id=category_id,
                                   item_id=item_id, i=toDeleteItem)


# =============================================================================#

@app.route('/categories/<int:category_id>/<int:item_id>')
def listItem(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id,
            category_id=category_id).one()
    return render_template('item.html', category_id=category_id,
                           item=item)


# =============================================================================#

def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# =============================================================================#

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# =============================================================================#

def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email'
            ]).one()
    return user.id


###############################################################################

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
