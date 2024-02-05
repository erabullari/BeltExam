from flask_app import app
from flask import render_template, request, session, redirect, flash
from flask_app.models.user import User
from flask_app.models.magazine import Magazine
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/controller')
    magazines=Magazine.get_all_magazines()
    
    data={
        'id':session['user_id']
    }
    user=User.get_user_by_id(data)
    return render_template("index.html", magazines=magazines,user=user)

@app.route('/controller')
def controller():
    if 'user_id' not in session:
        return redirect('/login')
    return redirect('/')



@app.route('/register')
def register():
    if 'user_id' in session:
        return redirect('/controller')
    return render_template("register.html")



@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
        return redirect('/login')
    return redirect('/login')


@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect('/controller')
    return render_template("login.html")


@app.route('/register', methods=['POST'])
def register_user():
    if 'user_id' not in session:
        if not User.validate_user(request.form):
            return redirect(request.referrer)
        
        password = request.form['password']
        pw_hash = bcrypt.generate_password_hash(password)
        data = {
            'email': request.form['email'],
            'firstName': request.form['firstName'],
            'lastName': request.form['lastName'],
            'password': pw_hash
        }
        session['user_id']= User.save_user(data)
        return redirect('/controller')
    return redirect('/controller')





@app.route('/login', methods=['POST'])
def login_user():
    if 'user_id' not in session:
        data = {
            'email': request.form['email']
        }
        user_in_db = User.get_user_info_by_email(data)
        if not user_in_db:
            flash("Invalid Email",'emailError')
            return redirect('/login')
        if not bcrypt.check_password_hash(user_in_db['password'], request.form['password']):
            flash("Invalid Password",'passwordError')
            return redirect('/login')
        session['user_id'] = user_in_db['id']
        return redirect('/controller')
    return redirect('/controller')



@app.route('/profile/<int:id>')
def profile(id):
    if 'user_id' not in session:
        return redirect('/controller')
    if id != session['user_id']:
        return redirect('/controller')
    data={
        'id':id,
    }
    user=User.get_user_by_id(data)

    subscriptions=Magazine.get_all_subscriptions(data)
    number = Magazine.get_sub_for_each_magazine(data)
    return render_template("profile.html",user=user,subscriptions=subscriptions)



@app.route('/edit/<int:id>', methods=['POST'])
def edit_user(id):
    if 'user_id' not in session:
        return redirect('/controller')
    if id != session['user_id']:
        return redirect('/controller')
    if User.validate_updated_user(request.form):
        return redirect(request.referrer)
    
    data={
        
        'id':id,
        'firstName':request.form['firstName'],
        'lastName':request.form['lastName'],
        'email':request.form['email']
    }
    User.edit_user(data)
    
    return redirect(request.referrer)
