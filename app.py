from flask import Flask, jsonify, redirect, render_template, request, session, url_for, json
import hashlib
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

def parse_data(data, columns):
    results = []
    for row in data:
        l = {}
        for i in range(len(columns)):
            l[columns[i]] = row[i]
        results.append(l)
    return jsonify({'data': results})

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
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, username, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ), t3 as ( \n select place, cityid, num_rating, rating, in_favourite, ( \n case \n when (username, place, cityid) in (select username, place, cityid from userratings) then 1 \n else 0 \n end\n) as is_rated\n from t2) select place, cityname, state, num_rating, rating, in_favourite, is_rated \n from t3, cities \n where t3.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' order by rating desc, num_rating desc"
    elif city == "":
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, username, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ), t3 as ( \n select place, cityid, num_rating, rating, in_favourite, ( \n case \n when (username, place, cityid) in (select username, place, cityid from userratings) then 1 \n else 0 \n end\n) as is_rated\n from t2) select place, cityname, state, num_rating, rating, in_favourite, is_rated \n from t3, cities \n where t3.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' and state = \'" + state + "\' order by rating desc, num_rating desc"
    else:
        s = "with t0 as (\n select * \n from FavouritePlaces \n where username = \'" + username + "\'), \n t1 as ( \n select places.place, places.cityid, num_rating, rating, username \n from places left outer join t0 \n on places.place = t0.place and places.cityid = t0.cityid\n ), t2 as ( \n select place, cityid, num_rating, rating, username, ( \n case \n when username is not null then 1 \n else 0 \n end\n) as in_favourite from t1 \n ), t3 as ( \n select place, cityid, num_rating, rating, in_favourite, ( \n case \n when (username, place, cityid) in (select username, place, cityid from userratings) then 1 \n else 0 \n end\n) as is_rated\n from t2) select place, cityname, state, num_rating, rating, in_favourite, is_rated \n from t3, cities \n where t3.cityid = cities.cityid and place like \'" + search_query + "\' || \'%\' and state = \'" + state + "\' and cityname = \'" + city + "\' order by rating desc, num_rating desc"
    
    cursor = conn.cursor()
    cursor.execute(s)
    data = cursor.fetchall()
    cursor.close()
    columns = ["place", "cityname", "state",
               "num_rating", "rating", "in_favourite"]
    
    return parse_data(data, columns)

@app.route('/update_rating')
def update_rating():
    username = request.form['username']
    cityname = request.form['cityname']
    place = request.form['place']
    state = request.form['state']
    rating = request.form['rating']
    cityid = ""
    lastrating = 0
    firsttimerating = 0

    s = "select cityid from cities where cityname = '" + cityname + "' and state = '" + state + "'"
    print(s)
    print()
    cur.execute(s)
    for row in cur:
        cityid = str(row[0])
    
    s = "select * from userratings where cityid = '" + cityid + "' and place = '" + place + "' and username = '" + username + "'"
    print(s)
    print()
    cur.execute(s)
    count = 0
    for row in cur:
        count += 1
        lastrating = row[3]

    if(count > 0):
        s = ""
        s = "update userratings \nset rating = '" + rating + "'\nwhere cityid = '" + cityid + "' and place = '" + place + "' and username = '" + username + "'"
        print(s)
        print()
        cur.execute(s)
    else:
        firsttimerating = 1
        s = "insert into userratings values('" + username + "', '" + place + "', '" + cityid + "', '" + rating + "')"
        print(s)
        print()
        cur.execute(s)

    deltarating = rating - lastrating
    
    s = "update places set rating = (num_rating * rating + " + str(deltarating) + ")/ (num_rating + " + str(firsttimerating) + ") , num_rating = num_rating + " + str(firsttimerating) + "\nwhere places.cityid = '" + cityid + "' and places.place = '" + place + "'"
    print(s)
    print()
    cur.execute(s)

    return jsonify({'data': 'success'})

    


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
    cities = json.loads(request.args.get('cities'))
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

    cityList = "("
    for i in range(len(cities)):
        cityList += "'"+cities[i]+"'"
        if(i < len(cities) - 1):
            cityList += ", "
    cityList += ")"
    
    s = "with t1 as (\n    select distinct name, locality \n    from cuisines_table \n    where name like \'" + query + "\' || \'%\'"
    if(len(cuisineList)>2):
        s+=" and cuisine in " + cuisineList 
    s+="\n)\nselect t1.name, t1.locality, cost, cuisine, rating, votes as num_rating \nfrom restaurants, t1, cities \nwhere t1.name = restaurants.name and t1.locality = restaurants.locality and rating >= " + minRating + " and cost <= " + maxCost + " and restaurants.cityid = cities.cityid"
    if(len(cityList)>2):
        s+=" and cityname in " + cityList 
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

@app.route('/recommend_restaurants')
def recommend_restaurants():
    locality = request.args.get('locality')
    # Perform search for Restaurants and return results
    # ...
    s = "with T2 as(\n    select name, restaurants.locality, cost, cuisine, rating, votes as num_rating, '" + locality+"'::text as hotel_locality,regexp_split_to_table(restaurants.locality, ',') as restaurant_locality\n    from restaurants\n)\nselect name, locality, cost, cuisine, rating, num_rating \nfrom T2 \nwhere position( LOWER(TRIM(restaurant_locality) ) in LOWER(hotel_locality)) > 0;"
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
        hashPass = str(hashlib.sha256(password.encode()).hexdigest())

        s = "select * from users\nwhere username = '" + username + "' and password = '" + hashPass + "'"
        print(s)
        cur.execute(s)
        count = 0
        for _ in cur:
            count+=1
        print(count)

        # check if user exists and password is correct
        if count > 0:
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
        name = request.form['name']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')
        
        if len(password) < 8:
            return render_template('signup.html', error='Passwords length must be atleast 8 characters')

        # check if user already exists
        s = "select * from users\nwhere username = '" + username + "'"
        print(s)
        cur.execute(s)
        count = 0
        for _ in cur:
            count+=1
        if count > 0:
            return render_template('signup.html', error='Username already taken')
        else:
            # create new user
            hashPass = str(hashlib.sha256(password.encode()).hexdigest())
            s = "insert into users values('" + username + "', '" + name + "', '" + hashPass + "')"
            cur.execute(s)
            conn.commit()
            print(s)
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
    query = "SELECT DISTINCT state FROM cities, places WHERE places.cityid = cities.cityid ORDER BY state ASC"

    cursor = conn.cursor()
    cursor.execute(query)
    states = cursor.fetchall()
    cursor.close()
    return jsonify({'data': states})


@app.route('/get_cities')
def get_cities():
    state = request.args.get('state')
    query = "with citiesInState as (select cityid, cityname from cities where state = \'" + state + "\'), pointsToCity as (select places.cityid, citiesInState.cityname, sum(places.rating * places.num_rating)/sum(places.num_rating) as rating, sum(num_rating) as num_rating from citiesInState, places where citiesInState.cityid = places.cityid group by places.cityid, citiesInState.cityname) select cityname, rating, num_rating from pointsToCity order by rating desc, num_rating desc, cityname asc"

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    columns = ["cityname", "rating", "num_rating"]
    return parse_data(data, columns)

@app.route('/get_places_recommendations')
def get_places_recommendations():

    username = request.args.get('user')

    q1 = "select place, cityname, state, rating, num_rating from places, cities where places.cityid = cities.cityid and num_rating >= 50 order by rating desc, num_rating desc limit 20"
    q2 = "with t1 as (select Place, cityid from FavouritePlaces where username = \'" + username + "\'), t2 as (select username, count(*) as num_overlaps from FavouritePlaces, t1 where t1.Place = FavouritePlaces.Place and t1.cityid = FavouritePlaces.cityid group by username), t3 as (select place, cityid, sum(power(2, num_overlaps)) as weight from FavouritePlaces, t2 where (place, cityid) not in (select place, cityid from t1) and t2.username = FavouritePlaces.username group by place, cityid) select t3.place, cityname, state, rating, num_rating from t3, places, cities where t3.place = places.place and t3.cityid = places.cityid and t3.cityid = cities.cityid order by weight desc, rating desc, num_rating desc, place asc, t3.cityid asc limit 20"

    if username == '':        
        query = q1
    else:
        query = q2

    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    columns = ['place', 'city', 'state', 'rating', 'num_rating']

    if len(data) == 0:
        cursor = conn.cursor()
        cursor.execute(q1)
        data = cursor.fetchall()
        cursor.close()
        return parse_data(data, columns)
    else:
        return parse_data(data, columns)
    
@app.route('/add_to_favourite', methods=['POST'])
def add_to_favourite():
    if 'user' not in session:
        return jsonify({'data': 'fail'})
    else:
        username = session['user']
        place = request.form.get('place')
        cityname = request.form.get('cityname')
        state = request.form.get('state')

        city_id_query = "select cityid from cities where cityname = \'" + cityname + "\' and state = \'" + state + "\'"
        cursor = conn.cursor()
        cursor.execute(city_id_query)
        cityid = cursor.fetchone()[0]
        cursor.close()

        query = "insert into FavouritePlaces values(\'" + username + "\', \'" + place + "\', " + str(cityid) + ")"
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return jsonify({'data': 'success'})
    
@app.route('/remove_from_favourite', methods=['POST'])
def remove_from_favourite():
    if 'user' not in session:
        return jsonify({'data': 'fail'})
    else:
        username = session['user']
        place = request.form.get('place')
        cityname = request.form.get('cityname')
        state = request.form.get('state')

        city_id_query = "select cityid from cities where cityname = \'" + cityname + "\' and state = \'" + state + "\'"
        cursor = conn.cursor()
        cursor.execute(city_id_query)
        cityid = cursor.fetchone()[0]
        cursor.close()

        query = "delete from FavouritePlaces where username = \'" + username + "\' and place = \'" + place + "\' and cityid = " + str(cityid)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        cursor.close()
        return jsonify({'data': 'success'})