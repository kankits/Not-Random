from flask import Flask, jsonify, redirect, render_template, request, session, url_for, json
import psycopg2

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


@app.route("/places_results")
def places_results():
    state = request.args.get('state')
    city = request.args.get('city')
    search_query = request.args.get('search_query')
    return render_template("places_results.html", active_tab="places", search_query=search_query, state=state, city=city)


@app.route("/places_states")
def places_states():
    return render_template("places_states.html", active_tab="places")


@app.route("/places_cities")
def places_cities():
    state = request.args.get('state')
    return render_template("places_cities.html", active_tab="places", state=state)


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
    search_query = request.args.get('search_query')
    state = request.args.get('state')
    city = request.args.get('city')
    username = request.args.get('user')
    # Perform search for Places and return results
    # ...
    if state == "" and city == "":
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ) select place, cityname, state, num_rating, rating, in_favourite \n from t2, cities \n where t2.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' limit 5"
    elif city == "":
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ) select place, cityname, state, num_rating, rating, in_favourite \n from t2, cities \n where t2.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' and state = \'" + state + "\' limit 5"
    else:
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ) select place, cityname, state, num_rating, rating, in_favourite \n from t2, cities \n where t2.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' and state = \'" + state + "\' and cityname = \'" + city + "\' limit 5"
    
    cur.execute(s)
    results = []
    columns = ["place", "cityname", "state",
               "num_rating", "rating", "in_favourite"]
    for row in cur:
        l = {}
        for i in range(len(columns)):
            l[columns[i]] = row[i]
        results.append(l)
    return jsonify({'data': results})


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
    s = "select name, locality, cost, cuisine, rating, votes as num_rating from restaurants where name like \'" + query + "\' || \'%\';"
    print(s)
    cur.execute(s)
    results = []
    columns = ["name", "locality", "cost", "cuisine", "rating", "num_rating"]
    for row in cur:
        l = {}
        for i in range(len(columns)):
            l[columns[i]] = row[i]
            if columns[i] == 'cuisine':
                l[columns[i]] = [i.strip() for i in l[columns[i]].split(',')]
            if columns[i] == 'cost':
                l[columns[i]] = "Rs. " + str(l[columns[i]])
        results.append(l)
    print(results)
    return jsonify({'data': results})

@app.route('/filter_restaurants')
def filter_restaurants():
    query = request.args.get('search')
    maxCost = request.args.get('maxCost')
    minRating = request.args.get('minRating')
    cuisines = json.loads(request.args.get('cuisines'))
    if(maxCost == ""):
        maxCost = "1000000000"
    if(minRating == ""):
        minRating = "0"
    
    cuisineList = "("
    for i in range(len(cuisines)):
        cuisineList += "'"+cuisines[i]+"'"
        if(i < len(cuisines) - 1):
            cuisineList += ", "
    cuisineList += ")"
    
    s = "with t1 as (\n    select distinct name, locality \n    from cuisines_table \n    where name like \'" + query + "\' || \'%\'"
    if(len(cuisineList)>2):
        s+=" and cuisine in " + cuisineList 
    s+="\n)\nselect t1.name, t1.locality, cost, cuisine, rating, votes as num_rating \nfrom restaurants, t1 \nwhere t1.name = restaurants.name and t1.locality = restaurants.locality and rating >= " + minRating + " and cost <= " + maxCost
    print(s)
    cur.execute(s)
    results = []
    columns = ["name", "locality", "cost", "cuisine", "rating", "num_rating"]
    for row in cur:
        l = {}
        for i in range(len(columns)):
            l[columns[i]] = row[i]
            if columns[i] == 'cuisine':
                l[columns[i]] = [i.strip() for i in l[columns[i]].split(',')]
            if columns[i] == 'cost':
                l[columns[i]] = "Rs. " + str(l[columns[i]])
        results.append(l)
    # print(results)
    return jsonify({'data': results})


@app.route('/search_travel')
def search_travel():
    src = request.args.get('src')
    dst = request.args.get('dst')
    displayTransportDetails = request.args.get('trdetails')
    mode = request.args.get('mode')
    s = ""
    columns = ["path", "length"]
    if(displayTransportDetails == "false"):
        s += "with recursive t3 as (\n    "
        if(mode != "Train"):
            s += "select distinct source_cityid as source, destination_cityid as destination, 'Flight' as typeOfTravel\n    from flights"
        if(mode == "Both"):
            s += "\n\n    union\n\n    "
        if(mode != "Flight"):
            s+="select distinct s1.cityid as source, s2.cityid as destination, 'Train' as typeOfTravel\n    from stations as s1, stations as s2, trainpath as x1, trainpath as x2, traininfo\n    where x1.train_no = x2.train_no and x1.seq < x2.seq and x1.station_code = s1.station_code and\n          x2.station_code = s2.station_code and x1.train_no = traininfo.train_no"
        s += "\n),\nt1 as (\n    select c1.cityname as source, c2.cityname as destination, typeOfTravel\n    from t3, cities as c1, cities as c2\n    where t3.source = c1.cityid and t3.destination = c2.cityid\n),\nt2(dst, path, len) as (\n    select t1.destination, ARRAY[t1.source::text, t1.typeOfTravel::text, t1.destination::text] as path, 1 as len\n    from t1\n    where t1.source = \'" + src + "\'\n\n    union all\n\n    select f.destination, (g.path || ARRAY[f.typeOfTravel::text, f.destination::text]), g.len + 1\n    from t1 as f join t2 as g on f.source = g.dst and f.destination != ALL(g.path) and g.len < 3\n)\n"
        s+="select path, len\nfrom t2\nwhere dst = \'" + dst + "\'\norder by len limit 5;"
        # s+="select * from t1 where source = 'Kolkata' and destination = 'Mumbai'"
    else:
        s += "with recursive t3 as (\n    "
        if(mode != "Train"):
            s += "select source_cityid as source, destination_cityid as destination, 'Flight' as typeOfTravel,\n           flight_number || ' , ' ||airline as transportid\n    from flights"
        if(mode == "Both"):
            s += "\n\n    union\n\n    "
        if(mode != "Flight"):
            s+="select s1.cityid as source, s2.cityid as destination, 'Train' as typeOfTravel,\n           traininfo.train_no || ' , ' || traininfo.train_name as transportid\n    from stations as s1, stations as s2, trainpath as x1, trainpath as x2, traininfo\n    where x1.train_no = x2.train_no and x1.seq < x2.seq and x1.station_code = s1.station_code and\n          x2.station_code = s2.station_code and x1.train_no = traininfo.train_no"
        s += "\n),\nt1 as (\n    select c1.cityname as source, c2.cityname as destination, typeOfTravel, transportid\n    from t3, cities as c1, cities as c2\n    where t3.source = c1.cityid and t3.destination = c2.cityid\n),\nt2(dst, path, len) as (\n    select t1.destination, ARRAY[t1.source::text, t1.typeOfTravel::text, t1.transportid::text, t1.destination::text] as path, 1 as len\n    from t1\n    where t1.source = \'" + src + "\'\n\n    union all\n\n    select f.destination, (g.path || ARRAY[f.typeOfTravel::text, f.transportid::text, f.destination::text]), g.len + 1\n    from t1 as f join t2 as g on f.source = g.dst and f.destination != ALL(g.path) and g.len < 2\n)\n"
        s+="select path, len\nfrom t2\nwhere dst = \'" + dst + "\'\norder by len limit 5;"
        # s+="select * from t1 where source = 'Kolkata' and destination = 'Mumbai'"
    # Perform search for Travel and return results
    # ...
    print(s)
    cur.execute(s)
    results = []
    for row in cur:
        l = {}
        for i in range(len(columns)):
            l[columns[i]] = row[i]
        results.append(l)
    print(results)    
    return jsonify({'data': results})


def get_candidate_values(column, table, query):
    s = "select " + column + " from " + table + " where " + \
        column + " like \'" + query + "\' || \'%\' limit 5"
    print(s)
    cur.execute(s)
    # values = ['abc', 'def', 'ghi']
    return [row[0] for row in cur]
    # return ["abc", "def", "ijk"]


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

# get states


@app.route('/get_states')
def get_states():
    cur.execute(
        "SELECT DISTINCT state FROM cities, places WHERE places.cityid = cities.cityid ORDER BY state ASC")
    # cur.execute("SELECT DISTINCT cityname FROM cities WHERE state = \'Karnataka\'")
    states = cur.fetchall()
    return jsonify({'data': states})


@app.route('/get_cities')
def get_cities():
    state = request.args.get('state')
    print(state)
    cur.execute("SELECT DISTINCT cityname FROM cities, places WHERE places.cityid = cities.cityid AND state = \'" +
                state + "\' ORDER BY cityname ASC")
    cities = cur.fetchall()
    print(cities)
    return jsonify({'data': cities})
