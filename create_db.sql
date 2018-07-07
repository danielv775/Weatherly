
/* Users */
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);


CREATE TABLE Population_Zip (
    id SERIAL PRIMARY KEY,
    zip INTEGER NOT NULL,
    population INTEGER NOT NULL,
    location_id INTEGER REFERENCES Locations
);


CREATE TABLE Locations (
    id SERIAL PRIMARY KEY,
    city VARCHAR NOT NULL,
    state VARCHAR NOT NULL,
    lat DECIMAL NOT NULL,
    long DECIMAL NOT NULL,
);

CREATE TABLE CheckIn (
    id SERIAL PRIMARY KEY,
    check_in_count INTEGER DEFAULT 0,
    location_id INTEGER REFERENCES Population_Zip
);


CREATE TABLE Comments (
    id SERIAL PRIMARY KEY,
    comment VARCHAR NOT NULL,
    user_id INTEGER REFERENCES Users
);