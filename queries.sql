--------recommend places----------
\set username ''

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
where (place, cityid) not in (select (place, cityid) from t1) and t2.username = FavouritePlaces.username
group by place, cityid
order by weight desc, place asc, cityid asc;



--------validate registration-----
\set username ''

select 
case
when exists (
    select *
    from Users
    where username = :username
) then false::boolean
else true::boolean
end as valid;


---------register user------------
\set username ''
\set Name ''
\set password''

insert into Users(usernamem, Name, password)
values (:username, :Name, :password);


---------authenticate login-------
\set username ''
\set password ''

select 
case
when exists (
    select *
    from Users
    where username = :username and password = :password
) then true::boolean
else false::boolean
end as valid;


--------add place to favourites----
\set username ''
\set Place ''
\set CityId 1

insert into FavouritePlaces(username, place, cityid)
select :username, :place, :cityid
where not exists (select * from FavouritePlaces where username = :username and place = :place and cityid = :cityid);

