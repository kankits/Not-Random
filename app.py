from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import psycopg2
import json

# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

conn = psycopg2.connect(
    host="10.17.51.34",
    database="group_34",
    user="group_34",
    password="ZiVNyMU7Jgrlfm"
)

cur = conn.cursor()


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
    s = "select place, cityname, state, num_rating, rating, 0 as in_favourite from places, cities where places.cityid = cities.cityid and place like \'" + query + "\' || \'%\' limit 5"
    cur.execute(s)
    results = []
    columns = ["place", "cityname", "state", "num_rating", "rating", "in_favourite"]
    for row in cur:
        l = {}
        for i in range(6):
            l[columns[i]] = row[i]
        results.append(l)
    # print(results)
    # results = [row[0] for row in cur]
    #return render_template('places.html', results=jsonify({'data':results}))
    return jsonify({'data': results})

@app.route('/search_hotels')
def search_hotels():
    query = request.args.get('search')
    rent = request.args.get('maxRent')
    rating = request.args.get('minRating')
    cities = json.loads(request.args.get('citiesFilter'))
    facilities = json.loads(request.args.get('facilitiesFilter'))
    print(facilities, cities)
    # Perform search for Hotels and return results
    # ...
    a = ''
    b = ''
    c = ''
    d = ''

    if len(cities) > 0 : 
        for i in range(len(cities)-1):
            a += 'cities.cityname = ' + cities[i] + ' and '

        if len(cities) > 0 :
            a += 'cities.cityname = \'' + cities[-1] + '\''

    if len(rating) > 0:
        b = 'starrating >= ' + rating 

    if len(rent) > 0:
        c = 'rent <= ' + rent 
    
    if len(facilities) > 0 :
        for i in range(len(facilities)-1) :
            if i == 'Free Wifi' : d += 'freewifi = true and '
            if i == "Free Breakfast" : d += 'freebreakfast = true and '
            if i ==  "Swimming Pool" : d += 'hasswimmingpool = true and ' 
        i = facilities[-1]
        if i == 'Free Wifi' : d += 'freewifi = true '
        if i == "Free Breakfast" : d += 'freebreakfast = true '
        if i ==  "Swimming Pool" : d += 'hasswimmingpool = true ' 

    cond = []
    if len(a) > 0 : cond.append(a) 
    if len(b) > 0 : cond.append(b)
    if len(c) > 0 : cond.append(c)
    if len(d) > 0 : cond.append(d)

    conditions = ''

    for i in range(len(cond)) : 
        conditions += cond[i] + ' and '

    s = "select hotelname,locality, cityname, starrating, freewifi, freebreakfast, hasswimmingpool, hoteldescription, hotelpincode, rent from hotels, cities where hotels.cityid = cities.cityid and " + conditions  + " hotelname like \'" + query + "\' || \'%\' limit 5"
    cur.execute(s)
    results = []
    columns = ["hotelname", "locality", "cityname", "starrating", "freewifi", "freebreakfast", "hasswimmingpool", "hoteldescription","hotelpincode", "rent"]
    for row in cur:
        l = {}
        for i in range(10) :
            l[columns[i]] = row[i]
        results.append(l)
    print(results)
    # results = ['search_hotels']
    # return render_template('hotels.html', results=results)
    return jsonify({'data': results})

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

def get_candidate_values(column, table, query):
    s = "select " + column + " from " + table + " where " + column + " like \'" + query +  "\' || \'%\' limit 5"
    print(s)
    cur.execute(s)
    # values = ['abc', 'def', 'ghi']
    return [row[0] for row in cur]
    #return ["abc", "def", "ijk"]


@app.route('/get_candidate_values')
def get_candidate_values_route():
    column = request.args.get('column')
    table = request.args.get('table')
    query = request.args.get('query')
    values = get_candidate_values(column, table, query)
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