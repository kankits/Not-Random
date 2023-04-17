DROP TABLE IF EXISTS raw_cities;
DROP TABLE IF EXISTS Raw_Places;
DROP TABLE IF EXISTS Raw_Hotels;
DROP TABLE IF EXISTS raw_restaurants;
DROP TABLE IF EXISTS raw_flights;
DROP TABLE IF EXISTS raw_trains;
DROP TABLE IF EXISTS raw_stations;

CREATE TABLE raw_cities (
    CityName varchar NOT NULL,
    State varchar NOT NULL
);

CREATE TABLE raw_places (
    CityName varchar NOT NULL,
    Place varchar NOT NULL,
    Rating int NOT NULL
);

CREATE TABLE raw_hotels (
    CityName varchar NOT NULL,
    HotelName varchar NOT NULL,
    RoomRent int NOT NULL,
    StarRating decimal NOT NULL,
    HotelAddress varchar NOT NULL,
    HotelPincode varchar NOT NULL,
    HotelDescription varchar NOT NULL,
    FreeWifi boolean NOT NULL,
    FreeBreakfast boolean NOT NULL,
    HasSwimmingPool boolean NOT NULL
);

CREATE TABLE raw_restaurants(
    Name varchar NOT NULL,
    Location varchar NOT NULL,
    Locality varchar NOT NULL,
    CityName varchar NOT NULL,
    Cuisine varchar NOT NULL,
    Rating decimal NOT NULL,
    Votes int NOT NULL,
    Cost int NOT NULL
);

CREATE TABLE raw_flights (
    flight_number varchar NOT NULL,
    airline varchar NOT NULL,
    origin_cityname varchar NOT NULL,
    destination_cityname varchar NOT NULL
);

CREATE TABLE raw_trains (
    train_no varchar NOT NULL,
    train_name varchar NOT NULL,
    seq int NOT NULL,
    station_code varchar NOT NULL, 
    station_name varchar NOT NULL,
    source_station_code varchar NOT NULL, 
    destination_station_code varchar NOT NULL
);

CREATE TABLE raw_stations (
    station_code varchar NOT NULL,
    station_name varchar NOT NULL,
    CityName varchar NOT NULL
);
---------------------------------------------------------------------------
DROP TABLE IF EXISTS Cities CASCADE;
DROP TABLE IF EXISTS Hotels CASCADE;
DROP TABLE IF EXISTS Places CASCADE;
DROP TABLE IF EXISTS Restaurants CASCADE;
DROP TABLE IF EXISTS Flights CASCADE;
DROP TABLE IF EXISTS Stations CASCADE;
DROP TABLE IF EXISTS TrainPath CASCADE;
DROP TABLE IF EXISTS TrainInfo CASCADE;

CREATE TABLE Cities (
    CityId int NOT NULL,
    CityName varchar NOT NULL,
    State varchar NOT NULL,
    PRIMARY KEY (CityId)
);

CREATE TABLE Hotels (
    Cityid int NOT NULL REFERENCES Cities(CityId),
    HotelName varchar NOT NULL,
    Locality varchar NOT NULL,
    StarRating decimal NOT NULL,
    Rent int NOT NULL,
    FreeBreakfast boolean NOT NULL,
    FreeWifi boolean  NOT NULL,
    HotelPincode varchar NOT NULL,
    HasSwimmingPool boolean NOT NULL,
    HotelDescription varchar NOT NULL,
    PRIMARY KEY (cityid, Hotelname, Locality)
);

CREATE TABLE Places (
    CityId int NOT NULL REFERENCES Cities(CityId),
    Place varchar NOT NULL,
    Rating decimal NOT NULL,
    num_rating int NOT NULL,
    PRIMARY KEY (Cityid, Place)
);

CREATE TABLE Restaurants(
    CityId int NOT NULL REFERENCES Cities(CityId),
    Name varchar NOT NULL,
    Locality varchar NOT NULL,
    Cost int NOT NULL,
    Cuisine varchar NOT NULL,
    Votes int NOT NULL,
    Rating decimal NOT NULL,
    PRIMARY KEY (CityId, Name, Locality)
);

CREATE TABLE Flights (
    flight_number varchar NOT NULL,
    airline varchar NOT NULL,
    source_cityid int NOT NULL REFERENCES Cities(CityId),
    destination_cityid int NOT NULL REFERENCES Cities(CityId),
    PRIMARY KEY (flight_number, airline)
);

CREATE TABLE Stations (
    CityId int NOT NULL REFERENCES Cities(CityId),
    station_code varchar NOT NULL,
    station_name varchar NOT NULL,
    PRIMARY KEY (station_code)
);

CREATE TABLE TrainInfo (
    train_no varchar NOT NULL,
    train_name varchar NOT NULL,
    source_station_code varchar NOT NULL REFERENCES Stations(station_code),
    destination_station_code varchar NOT NULL REFERENCES Stations(station_code),
    PRIMARY KEY (train_no)
);

CREATE TABLE TrainPath (
    train_no varchar NOT NULL REFERENCES TrainInfo(train_no),
    station_code varchar NOT NULL REFERENCES Stations(station_code),
    seq int NOT NULL,
    PRIMARY KEY (train_no, station_code)
);

CREATE TABLE Users (
    username varchar NOT NULL,
    Name varchar NOT NULL,
    password varchar NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE FavouritePlaces (
    username varchar NOT NULL REFERENCES Users(username),
    Place varchar NOT NULL,
    CityId int NOT NULL,
    constraint fk foreign key (CityId, Place) REFERENCES Places (CityId, Place),
    UNIQUE (username, Place, CityId)
);
