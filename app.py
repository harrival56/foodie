import os
from flask import Flask, render_template, request, session, g, flash
from werkzeug.utils import redirect
from werkzeug.wrappers import response
# from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Menu, Favorite
from forms import UserAddForm, LoginForm,  UserEditForm, MenuForm
from sqlalchemy.exc import IntegrityError

import requests

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql://:5433/foodie'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "no more a secret")
# toolbar = DebugToolbarExtension(app)
connect_db(app)

apiKey = "a1de5c39128c400a880f7e8337e23bc1"
search = "recipes/complexSearch"
find = "recipes/findByIngredients"
findByNutrient = "recipes/findByNutrients"
randomFind = "recipes/random"
url = "https://api.spoonacular.com/"

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup"""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
   
    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/")


@app.route('/menus')
def menu():
  user_id = g.user.id
  user = User.query.get(user_id)
  return render_template("menu.html", user=user)

@app.route('/favorites')
def favorites():
  user_id = g.user.id
  user = User.query.get(user_id)
  print(user.favorite)
  return render_template("favorite.html", user=user)

# response = {
#   "recipes": [
#     {
#       'id':23456,
#       'title': 'fake food',
#   'image':"https://spoonacular.com/recipeImages/716429-312x231.jpg",
#   'summary': "lorem ipsum dsjjjjkcmsi ksfdif kmvmvieeierr kekmrieemee krreike",
#   'aggregateLikes': 30
#     }
#   ]
# }

# recipes = {
#   'id':123345,
#   'title': "my fav fake food",
#   'image': "https://spoonacular.com/recipeImages/73420-312x231.jpg"
# }

@app.route("/user")
def user():
  if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
  id= g.user.id
  user = User.query.get(id)
  return render_template('user.html', user=user)

@app.route('/edit_profile', methods=["GET", "POST"])
def edit_profile():
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    user = g.user
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data

            db.session.commit()
            return redirect("/user")

        flash("Wrong password, please try again.", 'danger')

    return render_template('edit_user.html', form=form, user_id=user.id)
  
@app.route('/')
def home_page():
  querystring = {"number":"20","apiKey":apiKey}
  response = requests.request("GET", url + randomFind, params=querystring ).json()
  return render_template('recipes.html', recipes=response['recipes'])

@app.route('/search')
def get_recipe():
  if (str(request.args['search']).strip() != ""):
    queryString = {"query":request.args['search'],"number":20, "apiKey":apiKey}
    response = requests.request("GET", url + search, params=queryString).json()
    return render_template("recipes.html", recipes=response['results'])
  else:
    querystring = {"number":"20","ranking":"1","apiKey":apiKey}
    response = requests.request("GET", url + randomFind, params=querystring).json()
    return render_template('recipes.html', recipes=response['recipes'])

@app.route('/by_ingredients')
def get_recipes_by_ingredient():
  if (str(request.args['ingrdt']).strip() != ""):
      querystring = {"number":"20","ranking":"1","ingredients":request.args['ingrdt'],"apiKey":apiKey}
      response = requests.request("GET", url + find, params=querystring ).json()
      return render_template('recipes.html', recipes=response)
  else:
      # Random recipes
      querystring = {"number":"20","ranking":"1","apiKey":apiKey}
      response = requests.request("GET", url + randomFind, params=querystring).json()
      return render_template('recipes.html', recipes=response['recipes'])


@app.route('/recipe')
def get_recipe_detail():
  recipe_id = request.args['id']
  recipe_info_endpoint = "recipes/{0}/information".format(recipe_id)
  ingedientsWidget = "recipes/{0}/ingredientWidget".format(recipe_id)
  equipmentWidget = "recipes/{0}/equipmentWidget".format(recipe_id)
  winePairing = 'food/wine/pairing'
  
  queryKey = {'apiKey': apiKey}
  recipe_info = requests.request("GET", url + recipe_info_endpoint, params=queryKey).json()
  querystring = {"defaultCss":"true", "showBacklink":"false", "apiKey":apiKey}
  food = {'food':recipe_info['title'], 'apiKey':apiKey}
  recipe_info['inregdientsWidget'] = requests.request("GET", url + ingedientsWidget, params=querystring).text
  recipe_info['equipmentWidget'] = requests.request("GET", url + equipmentWidget, params=querystring).text
  recipe_info['winePairing'] = requests.request("GET", url + winePairing, params=food).json()
  # print(recipe_info['winePairing']['pairingText'])
  # pdb.set_trace()
  return render_template('recipe.html', recipe=recipe_info)

@app.route('/nutrients')
def nutrients():
  return render_template('search_by_nut.html')

@app.route('/by_nutrients')
def get_recipes_by_nutrient():
 
 queryString = {
   "minCarbs":request.args['minCarb'], 
   "maxCarbs":request.args['maxCarb'],
   "minCal":request.args['minCal'], 
   "maxCal":request.args['maxCarb'],
   "minProtein":request.args['minProtein'],
   "maxProtein":request.args['maxProtein'],
   "minFat":request.args['minFat'],
   "maxFat":request.args['maxFat'],
   "number":20, 
   "apiKey":apiKey
 }
 recipe_info = requests.request("GET", url + findByNutrient, params=queryString).json()
 return render_template("recipes.html", recipes=recipe_info)
@app.route('/add_fav', methods=["POST"])
def add_favorite():
  if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
  recipe_id = request.args['id']
  recipe_title = request.args['title']
  recipe_image = request.args['image']
  user_id = g.user.id

  new_fav = Favorite(recipe_id=recipe_id, title=recipe_title, image=recipe_image, user_id=user_id)
  db.session.add(new_fav)
  db.session.commit()
  return redirect("/favorites")
import pdb
@app.route('/add_menu', methods=["GET", "POST"])
def add_menu():
  if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
  user_id = g.user.id
  title = request.args['title']
  # recipe = {'title':title}
  form = MenuForm()
  if form.validate_on_submit():
    # recipe.title = form.title.data
    day = form.day.data
    time = form.time.data
    recipe_id = request.args['id']
    # title = request.args['title']
    pdb.set_trace()
    new_menu = Menu(day=day, time=time, title=title, user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_menu)
    db.session.commit()
    return redirect('/menus')

  return render_template('new_menu.html', form=form)

@app.route('/delete_fav')
def delete_fav():
  if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
  delete = Favorite.query.get(request.args['id'])
  db.session.delete(delete)
  db.session.commit()
  return redirect('/favorites')


@app.route('/delete_menu')
def delete_menu():
  if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")
  delete = Menu.query.get(request.args['id'])
  db.session.delete(delete)
  db.session.commit()
  return redirect('/menus')
