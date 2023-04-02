from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUT_TB_INTERCEPT_REDIRECTS']=False

connect_db(app)
app.app_context().push()

# GET /
@app.route("/")
def home():    
    return redirect("/users")

# GET /users  display list of user 
@app.route("/users")
def users():
    users = User.query.order_by(User.first_name, User.last_name).all()   
    return render_template("user.html", users=users)

# GET /users/new show an add form 
@app.route("/users/new", methods=["GET"])
def add_form():
    return render_template("new_user.html")

# POST /users/new  add new users form
@app.route("/users/new", methods=["POST"])
def new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    img_url = request.form['img_url']

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect ("/users")

# GET /users/[user-id] show user information
@app.route('/users/<int:user_id>')
def users_show(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_info.html', user=user)



#GET /users/[user-id]/edit show user edit page
@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

 
#POST /users/[user-id]/edit edit user information
@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.img_url = request.form["img_url"]

    db.session.add(user)
    db.session.commit()

    return redirect("/users")

#POST /users/[user-id]/delete delete a user from db
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect ("/users")



