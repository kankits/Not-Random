--1--
\set irating 4.0
\set irent 10000
\set ifreebreakfast true
\set ifreewifi true
\set ihasswimmingpool true
\set icities '(\'Nagpur\', \'Delhi\', \'Mumbai\',\'Hyderabad\', \'Ghaziabad\')'
select hotelname, cities.cityname as city
from hotels, cities
where hotels.cityid = cities.cityid and
      starrating >= :irating and
      rent <= :irent and
      freebreakfast = :ifreebreakfast and
      freewifi = :ifreewifi and
      hasswimmingpool = :ihasswimmingpool and
      cityname in :icities
order by hotelname;


--5--
\set istate '\'Rajasthan\''
with citiesInState as (
    select cityid, cityname
    from cities
    where state = :istate
), pointsToCity as (
    select places.cityid, citiesInState.cityname, avg(rating) as points
    from citiesInState, places
    where citiesInState.cityid = places.cityid
    group by places.cityid, citiesInState.cityname
)
select cityid, cityname
from pointsToCity
order by points desc, cityname asc;


--6--
\set ihotelname '\'FabHotel Pallavi New Delhi Station\''
\set ilocality '\'8572 Arakashan Road, Paharganj, New Delhi, Delhi N.C.R\''
\set icityid 140

with T2 as 
(
    select name, restaurants.locality, restaurants.cityid, :ilocality::text as hotel_locality, 
        regexp_split_to_table(restaurants.locality, ',') as restaurant_locality
    from restaurants
    where :icityid = restaurants.cityid 
)

select name , locality, cityid
from T2 
where position( LOWER(TRIM(restaurant_locality) ) in LOWER(hotel_locality)) > 0;


--7--
\set icityname '\'Nagpur\''
select place, cities.cityid
from places, cities
where places.cityid = cities.cityid
and cities.cityname = :icityname
order by rating desc, num_rating desc;

--3--
\set source '\'Mumbai\''
\set destination '\'Delhi\''
with recursive t3 as (
    select source_cityid as source, destination_cityid as destination, 'Flight' as typeOfTravel
    from flights

    union
    
    select s1.cityid as source, s2.cityid as destination, 'Train' as typeOfTravel
    from stations as s1, stations as s2, trainpath as x1, trainpath as x2, traininfo
    where x1.train_no = x2.train_no and x1.seq < x2.seq and x1.station_code = s1.station_code and 
          x2.station_code = s2.station_code and x1.train_no = traininfo.train_no
), 
t1 as (
    select c1.cityname as source, c2.cityname as destination, typeOfTravel
    from t3, cities as c1, cities as c2
    where t3.source = c1.cityid and t3.destination = c2.cityid
), 
t2(dst, path, len) as (
    select t1.destination, ARRAY[t1.source::text, t1.typeOfTravel::text, t1.destination::text] as path, 1 as len
    from t1
    where t1.source = :source

    union all 

    select f.destination, (g.path || ARRAY[f.typeOfTravel::text, f.destination::text]), g.len + 1
    from t1 as f join t2 as g on f.source = g.dst and f.destination != ALL(g.path) and g.len < 3
)
select *
from t2
where dst = :destination
order by len;

------
\set source '\'Mumbai\''
\set destination '\'Delhi\''
with recursive t3 as (
    select source_cityid as source, destination_cityid as destination, 'Flight' as typeOfTravel, 
           flight_number || ' , ' ||airline as transportid
    from flights

    union
    
    select s1.cityid as source, s2.cityid as destination, 'Train' as typeOfTravel, 
           traininfo.train_no || ' , ' || traininfo.train_name as transportid
    from stations as s1, stations as s2, trainpath as x1, trainpath as x2, traininfo
    where x1.train_no = x2.train_no and x1.seq < x2.seq and x1.station_code = s1.station_code and 
          x2.station_code = s2.station_code and x1.train_no = traininfo.train_no
), 
t1 as (
    select c1.cityname as source, c2.cityname as destination, typeOfTravel, transportid
    from t3, cities as c1, cities as c2
    where t3.source = c1.cityid and t3.destination = c2.cityid
), 
t2(dst, path, len) as (
    select t1.destination, 
           ARRAY[t1.source::text, t1.typeOfTravel::text, t1.transportid::text, t1.destination::text] as path, 1 as len
    from t1
    where t1.source = :source

    union all 

    select f.destination, 
           (g.path || ARRAY[f.typeOfTravel::text, f.transportid::text, f.destination::text]), g.len + 1
    from t1 as f join t2 as g on f.source = g.dst and f.destination != ALL(g.path) and g.len < 2
)
select *
from t2
where dst = :destination
order by len;

----------------
-- update rating--

\set irating 4.0
\set icityid 2
\set iplace '\'Delhi\''

UPDATE places SET rating = (num_rating * rating + :irating)/ (num_rating + 1) , num_rating = num_rating + 1
WHERE places.cityid = :icityid and places.place = :iplace;

-----------------
--hotel search---

\set ihotel '\'Taj\''

select hotelname,locality, cityname
from hotels, cities
where hotels.cityid = cities.cityid and hotelname like '%' || :ihotel || '%';

-----------------
--restaurant search--

\set irestaurant '\'Taj\''

select name,locality, cityname
from restaurants, cities
where restaurants.cityid = cities.cityid and name like '%' || :irestaurant || '%';

-----------------------
--place search---

\set iplace '\'Taj Mahal\''
select place, cityname
from places, cities
where cities.cityid = places.cityid and place like '%' || :iplace || '%';

------------------
--cuisine search------

\set icuisine '\'Italian\''

select cuisine
from cuisine_name
where cuisine like '%' || :icuisine || '%';

------------------
---city search ---

\set icity '\'Pune\''

select cityname, cityid
from cities
where cityname like '%' || :icity || '%';


--2--
\set irating 4.0
\set icost 1000
\set icities '(\'Nagpur\', \'Delhi\', \'Mumbai\',\'Hyderabad\', \'Ghaziabad\')'
\set icuisines '(\'Italian\', \'South Indian\')'
select distinct restaurants.name 
from restaurants, cities, cuisines_table
where restaurants.cityid = cities.cityid and
      cityname in :icities and
      rating >= :irating and
      cost <= :icost and
      cuisines_table.cityid = restaurants.cityid and 
      cuisines_table.name = restaurants.name and
      cuisines_table.locality = restaurants.locality and
      cuisines_table.cuisine in :icuisines
order by restaurants.name;


------validate registration-----
\set username '\'rainy\''

select 
case
when exists (
    select *
    from Users
    where username = :username
) then false::boolean
else true::boolean
end as valid;


-------register user------------
\set username '\'rainy\''
\set Name '\'giraffe\''
\set password '\'zebra\''

insert into Users(username, Name, password)
values (:username, :Name, :password);


-------authenticate login-------
\set username '\'rainy\''
\set password '\'zebra\''

select 
case
when exists (
    select *
    from Users
    where username = :username and password = :password
) then true::boolean
else false::boolean
end as valid;


------add place to favourites----
\set username '\'rainy\''
\set Place '\'Kadam Dam\''
\set CityId 4

insert into FavouritePlaces(username, place, cityid)
select :username, :Place, :CityId
where not exists (select * from FavouritePlaces where username = :username and place = :Place and cityid = :CityId);

--------recommend places----------
\set username '\'rainy\''

with t1 as
(
    select Place, cityid
    from FavouritePlaces
    where username = :username
),
t2 as
(
    select username, count(*) as num_overlaps
    from FavouritePlaces, t1
    where t1.Place = FavouritePlaces.Place and t1.cityid = FavouritePlaces.cityid
    group by username
)
select place, cityid, sum(power(2, num_overlaps)) as weight
from FavouritePlaces, t2
where (place, cityid) not in (select place, cityid from t1) and t2.username = FavouritePlaces.username
group by place, cityid
order by weight desc, place asc, cityid asc;


with t0 as (
    select * from FavouritePlaces
    where username = 'abc'
),
t1 as (
    select places.place, places.cityid, username
    from places left outer join t0
    on places.place = FavouritePlaces.place and places.cityid = FavouritePlaces.cityid
),
t2 as (
    select place, cityid, (
        case 
        when username is not null then 1
        else 0
        end;
    ) as in_favourite
    from t1
)
select place, city, state, num_rating, rating, in_favourite
from t2, cities
where t2.cityid = cities.cityid


select place, cityname, state, num_rating, rating, 0 as in_favourite
from places, cities
where places.cityid = cities.cityid
