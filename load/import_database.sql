COPY raw_cities from '/app/Not-Random/data/raw_cities.csv' DELIMITER ',' CSV HEADER;
COPY raw_places from '/app/Not-Random/data/raw_places.csv' DELIMITER ',' CSV HEADER;
COPY raw_hotels from '/app/Not-Random/data/raw_hotels.csv' DELIMITER ',' CSV HEADER;
COPY raw_restaurants from '/app/Not-Random/data/raw_restaurants.csv' DELIMITER ',' CSV HEADER;
COPY raw_flights from '/app/Not-Random/data/raw_flights.csv' DELIMITER ',' CSV HEADER;
COPY raw_trains from '/app/Not-Random/data/raw_trains.csv' DELIMITER ',' CSV HEADER;
COPY raw_stations from '/app/Not-Random/data/raw_stations.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select row_number() over (order by cityName) as CityId, CityName, State
    from raw_cities
)
to '/app/Not-Random/data/cities.csv'
csv header;

COPY cities from '/app/Not-Random/data/cities.csv' DELIMITER ',' CSV HEADER;

DROP VIEW IF EXISTS cities_unique;
CREATE VIEW cities_unique as (select min(cityid) as cityid, cityName from cities group by cityName);

COPY
(
    select
        Cityid,
        HotelName,
        min(HotelAddress) as Locality,
        min(starRating) as starRating,
        avg(roomrent) :: integer as rent,
        min(FreeBreakfast::integer)::boolean as FreeBreakfast,
        min(FreeWifi::integer)::boolean as FreeWifi,
        min(Hotelpincode) as pincode,
        min(HasSwimmingPool::integer)::boolean as HasSwimmingPool,
        min(HotelDescription) as HotelDescription

    from cities_unique, raw_hotels
    where raw_hotels.CityName = cities_unique.CityName or (raw_hotels.CityName = 'Bangalore' and cities_unique.CityName = 'Bengaluru') 
    group by cityid, HotelName
)
to '/app/Not-Random/data/hotels.csv'
csv header;

COPY hotels from '/app/Not-Random/data/hotels.csv' DELIMITER ',' CSV HEADER;


COPY 
(
    select cityid, place, avg(rating) as rating, count(*) as num_rating
    from Raw_Places, cities_unique
    where Raw_Places.cityName = cities_unique.cityname or (Raw_Places.CityName = 'Bangalore' and cities_unique.CityName = 'Bengaluru') 
    group by cityid, place
)
to '/app/Not-Random/data/places.csv'
csv header;

COPY places from '/app/Not-Random/data/places.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select
        cityid,
        Name,
        Location as Locality,
        min(Cost) as Cost,
        min(Cuisine) as Cuisine,
        min(Votes) as Votes,
        min(Rating) as Rating
    from raw_restaurants, cities_unique
    where raw_restaurants.cityName = cities_unique.cityname or (raw_restaurants.CityName = 'Bangalore' and cities_unique.CityName = 'Bengaluru') 
    group by cityid, Name, Location
)   
to '/app/Not-Random/data/restaurants.csv'
csv header;

COPY restaurants from '/app/Not-Random/data/restaurants.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select
        flight_number,
        airline,
        min(source_cities.cityid) as source_cityid,
        min(destination_cities.cityid) as destination_cityid
    from raw_flights, cities_unique as source_cities, cities_unique as destination_cities
    where
        (raw_flights.origin_cityname = source_cities.cityname or (raw_flights.origin_cityname = 'Bangalore' and source_cities.CityName = 'Bengaluru'))
        and
        (raw_flights.destination_cityname = destination_cities.cityname or (raw_flights.destination_cityname = 'Bangalore' and destination_cities.CityName = 'Bengaluru'))
    group by flight_number, airline
)   
to '/app/Not-Random/data/flights.csv'
csv header;

COPY flights from '/app/Not-Random/data/flights.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select
        min(CityId) as CityId,
        station_code,
        min(station_name) as station_name
    from raw_stations, cities_unique
    where
        raw_stations.CityName = cities_unique.cityname or (raw_stations.CityName = 'Bangalore' and cities_unique.CityName = 'Bengaluru')
    group by station_code
)   
to '/app/Not-Random/data/stations.csv'
csv header;

COPY stations from '/app/Not-Random/data/stations.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select
        train_no,
        min(train_name) as train_name,
        min(source_station_code) as source_station_code,
        min(destination_station_code) as destination_station_code
    from raw_trains
    where
        (source_station_code in (select station_code from stations))
        and
        (destination_station_code in (select station_code from stations))
    group by train_no
)   
to '/app/Not-Random/data/traininfo.csv'
csv header;

COPY TrainInfo from '/app/Not-Random/data/traininfo.csv' DELIMITER ',' CSV HEADER;

COPY
(
    select
        train_no,
        station_code,
        min(seq) as seq
    from raw_trains
    where
        (train_no in (select train_no from TrainInfo))
        and
        (station_code in (select station_code from stations))
    group by train_no, station_code
)   
to '/app/Not-Random/data/trainpath.csv'
csv header;

COPY TrainPath from '/app/Not-Random/data/trainpath.csv' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS raw_cities;
DROP TABLE IF EXISTS Raw_Places;
DROP TABLE IF EXISTS Raw_Hotels;
DROP TABLE IF EXISTS raw_restaurants;
DROP TABLE IF EXISTS raw_flights;
DROP TABLE IF EXISTS raw_trains;
DROP TABLE IF EXISTS raw_stations;


--create materialized view for cuisines---

CREATE MATERIALIZED VIEW cuisines_table
as
select cityid,name,locality, trim(regexp_split_to_table (cuisine, ',')) as cuisine
from restaurants ;

-----------------------

CREATE MATERIALIZED VIEW cuisine_name
as
select distinct cuisine
from cuisines_table  ;


-----Create indexes-----
create index idx1 on hotels(cityid, starrating, rent, freebreakfast, freewifi, hasswimmingpool);

create index idx2 on Restaurants(cityid, rating, cost, name, locality);

create index idx3 on cuisines_table(cityid,name,locality);

create index idx4 on cuisines_table(cuisine);

create index idx5 on cuisine_name(cuisine);

create index idx6 on cities(state);

create index idx7 on cities(cityname);

create index idx8 on places(rating, num_rating);

create index idx9 on TrainPath(train_no);

create index idx10 on TrainPath(station_code);

create index idx11 on FavouritePlaces(username);

create index idx12 on FavouritePlaces(place, cityid);

create index idx13 on Users(username, password);


-- drop index idx1, idx2, idx3, idx4,idx5,idx6, idx7, idx8, idx9, idx10,idx11, idx12, idx13;