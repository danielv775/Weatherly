
/* Users */
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);

/* Population and Zip codes
   This table has every unique location.
*/
CREATE TABLE Population_Zip (
    id SERIAL PRIMARY KEY,
    zip INTEGER NOT NULL,
    population INTEGER NOT NULL
);

/*
Locations
There is a 1-to-Many relationship between each location and each (Zip code, Population) Pair
*/
CREATE TABLE Locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    lat DECIMAL NOT NULL,
    long DECIMAL NOT NULL,
    location_id INTEGER REFERENCES Population_Zip
);

/* Keep track of Check in count for each unique zip code*/
CREATE TABLE CheckIn (
    id SERIAL PRIMARY KEY,
    check_in_count INTEGER DEFAULT 0,
    location_id INTEGER REFERENCES Population_Zip
);

/*
Comments
There is a Many-to-1 relationship between comments and users.
*/
CREATE TABLE Comments (
    id SERIAL PRIMARY KEY,
    comment VARCHAR NOT NULL,
    user_id INTEGER REFERENCES Users
);