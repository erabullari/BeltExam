from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.magazine import Magazine
from flask_app.models.user import User

@app.route('/magazines/new')
def magazines():
    if 'user_id' not in session:
        return redirect('/controller')
    return render_template("addMagazines.html")


@app.route('/addmagazines' , methods = ['POST'])
def addmagazines():
    if 'user_id' not in session:
        return redirect('/controller')
    if not Magazine.validate_magazine(request.form):
        return redirect(request.referrer)
    
    data ={
        'title': request.form['title'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }
    Magazine.save_magazine(data)
    return redirect('/controller')

@app.route('/show_magazines/<int:id>', methods=['POST','GET'])
def show_magazines(id):
    if 'user_id' not in session:
        return redirect('/controller')
    
    data1={
        'id':id
        }
    data2={
        'id':session['user_id']
    }
    user=User.get_user_by_id(data2)
    magazine=Magazine.get_magazine_by_id(data1)
    subscribed=Magazine.all_subscribed(data1)
    return render_template("showMagazine.html", magazine=magazine, user=user, subscribed=subscribed)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'user_id' not in session:
        return redirect('/controller')
    data={ 'id':id }
    magazines =Magazine.get_magazine_by_id(data)
    if magazines['user_id'] != session['user_id']:
        return redirect('/controller')
    Magazine.delete(data)
    return redirect('/controller')


#subscription
@app.route('/subscribe/<int:id>', methods=['POST','GET'])
def subscribe(id):
    if 'user_id' not in session:
        return redirect('/controller')
    data={
        'user_id':session['user_id'],
        'magazine_id':id
    }
    
    if Magazine.controlle(data):
        flash("You are already subscribed to this magazine.",'subscribeError')
        return redirect('/controller')
    Magazine.subscribe(data)
    return redirect('/controller')

@app.route('/deletesub/<int:id>', methods=['POST','GET'])
def deletesub(id):
    if 'user_id' not in session:
        return redirect('/controller')
    data={
        'user_id':session['user_id'],
        'magazine_id':id
    }
    Magazine.deletesub(data)
    return redirect(request.referrer)
