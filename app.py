from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)
###############################################################################
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
#=============================================================================#
engine = create_engine('sqlite:///categoriesmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
#=============================================================================#
DBSession = sessionmaker(bind = engine)
session = DBSession()
###############################################################################

@app.route('/categories/<int:category_id>/JSON')
def categoryJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Item=[i.serialize for i in items])


#=============================================================================#

@app.route('/')
@app.route('/categories/')
def listCategories():
    categories = session.query(Category)
    output = ''
    for c in categories :
        output+=c.name
        output+='</br>'
        items = session.query(Item).filter_by(category_id = c.id)
        for i in items:
            output+=i.name
            output+='</br>'
        output+='</br>'
    return output

#=============================================================================#

@app.route('/categories/<int:category_id>/')
def listCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    items = session.query(Item).filter_by(category_id = category_id)
    return render_template('category.html', category=category, items=items)

#=============================================================================#

@app.route('/categories/<int:category_id>/new', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method=='POST':
        item=Item(name = request.form['name'], category_id=category_id)
        session.add(item)
        session.commit()
        flash('new item is added!')
        return redirect(url_for('listCategory', category_id=category_id))
    else :
        return render_template('newItem.html', category_id=category_id)

#=============================================================================#

@app.route('/categories/<int:category_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    editedItem = session.query(Item).filter_by(id = item_id).one()
    if request.method=='POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('item is edited!')
        return redirect(url_for('listCategory', category_id=category_id))
    else :
        return render_template('editItem.html', category_id=category_id, item_id=item_id, i=editedItem)

#=============================================================================#

@app.route('/categories/<int:category_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(category_id, item_id):
    toDeleteItem = session.query(Item).filter_by(id = item_id).one()
    if request.method=='POST':
        session.delete(toDeleteItem)
        session.commit()
        flash('item is deleted!')
        return redirect(url_for('listCategory', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item_id=item_id, i=toDeleteItem)

###############################################################################

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
