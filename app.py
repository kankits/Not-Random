from flask import Flask, jsonify, redirect, render_template, request, session, url_for
 
# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def index():
    return render_template('index.html')
 
@app.route("/places")
def places():
    return render_template("places.html", active_tab="places")

@app.route("/hotels")
def hotels():
    return render_template("hotels.html", active_tab="hotels")

@app.route("/restaurants")
def restaurants():
    return render_template("restaurants.html", active_tab="restaurants")

@app.route("/travel")
def travel():
    return render_template("travel.html", active_tab="travel")

@app.route('/search_places')
def search_places():
    query = request.args.get('search')
    # Perform search for Places and return results
    # ...
    results = ['search_places']
    return render_template('places.html', results=results)

@app.route('/search_hotels')
def search_hotels():
    query = request.args.get('search')
    # Perform search for Hotels and return results
    # ...
    results = ['search_hotels']
    return render_template('hotels.html', results=results)

@app.route('/search_restaurants')
def search_restaurants():
    query = request.args.get('search')
    # Perform search for Restaurants and return results
    # ...
    results = ['search_restaurants']
    return render_template('restaurants.html', results=results)

@app.route('/search_travel')
def search_travel():
    query = request.args.get('search')
    # Perform search for Travel and return results
    # ...
    results = ['search_travel']
    return render_template('travel.html', results=results)

def get_candidate_values(column, query):
    values = ['abc', 'def', 'ghi']
    return values


@app.route('/get_candidate_values')
def get_candidate_values_route():
    column = request.args.get('column')
    query = request.args.get('query')
    values = get_candidate_values(column, query)
    return jsonify({'data': values})

# Temporary Users table

Users = {"admin": "admin"}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # check if user exists and password is correct
        if username in Users.keys() and Users[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')

# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        # check if user already exists
        if username in Users.keys():
            return render_template('signup.html', error='Username already taken')
        else:
            # create new user
            Users[username] = password
            session['user'] = username
            return redirect(url_for('dashboard'))
    else:
        return render_template('signup.html')

# dashboard page (requires authentication)
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        return redirect(url_for('login'))

# logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))