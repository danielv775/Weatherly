from pandas import read_csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def read_data():
    return read_csv("zips_updated.csv")

def create_tables():

    # Create Users Table
    db.execute('CREATE TABLE users ('
               'id SERIAL PRIMARY KEY,'
               'username VARCHAR NOT NULL,'
               'pw_hash VARCHAR NOT NULL);')

    # Create Locations
    db.execute('CREATE TABLE locations ('
            'id SERIAL PRIMARY KEY,'
            'zipcode VARCHAR NOT NULL,'
            'city VARCHAR NOT NULL,'
            'state VARCHAR NOT NULL,'
            'lat DECIMAL NOT NULL,'
            'long DECIMAL NOT NULL,'
            'population INTEGER NOT NULL);')

    db.commit()

    # Create Comments Table
    db.execute('CREATE TABLE comments ('
               'id SERIAL PRIMARY KEY,'
               'comment VARCHAR NOT NULL,'
               'user_id INTEGER REFERENCES users(id),'
               'location_id INTEGER REFERENCES locations(id));')

    db.commit()


def main():

    # Create DB Tables
    create_tables()

    # Read Location Data
    data_df = read_data()
    data_df.columns = ["zipcode", "city", "state", "lat", "long", "population"]
    data_df["zipcode"] = data_df["zipcode"].astype(str)

    # Cast Zipcode to string and add leading zeros to zip codes of length 4
    mask = (data_df["zipcode"].str.len() == 4)
    data_df.loc[mask, "zipcode"] = data_df.loc[mask, "zipcode"].apply(lambda zip_code: f"0{zip_code}")

    '''
    # Ensure all zip codes are 5 digit strings
    mask_two = (data_df["zipcode"].str.len() == 5)
    print(len(data_df.loc[mask_two, "zipcode"]))
    '''

    # Insert each row from zips_updated.csv into Locations table
    for row in data_df.iterrows():
        zip_code = row[1][0]
        city = row[1][1]
        state = row[1][2]
        lat = row[1][3]
        longg = row[1][4]
        population = row[1][5]

        db.execute("INSERT INTO locations (zipcode, city, state, lat, long, population) VALUES (:zip_code, :city, :state, :lat, :long, :population)",
                  {"zip_code": zip_code, "city": city, "state": state, "lat": float(lat), "long": float(longg), "population": population})
        print(f"Added location with Zipcode: {zip_code}, City: {city}, State: {state}, lat: {lat}, long: {longg}, population: {population}")

    db.commit()


    '''
    to_sql not working
    population_zip_df.to_sql(name="population_zip", con=engine, index=False, index_label="id", if_exists="append")
    locations_df.to_sql(name="locations", con=engine, index=False, index_label="id", if_exists="append")
    '''

if __name__ == "__main__":
    main()