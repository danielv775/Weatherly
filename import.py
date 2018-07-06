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
    return read_csv("zips.csv")

def main():
    data_df = read_data()

    population_zip_df = data_df[["Zipcode", "Population"]]
    population_zip_df.columns = ["zip", "population"]
    locations_df = data_df[["City", "State", "Lat", "Long"]]
    locations_df.columns = ["city", "state", "lat", "long"]

    '''
    to_sql not working
    population_zip_df.to_sql(name="population_zip", con=engine, index=False, index_label="id", if_exists="append")
    locations_df.to_sql(name="locations", con=engine, index=False, index_label="id", if_exists="append")
    '''

    for row in population_zip_df.iterrows():
        zip_code = row[1][0]
        population = row[1][1]

        db.execute("INSERT INTO population_zip (zip, population) VALUES (:zip_code, :population)",
                    {"zip_code": int(zip_code), "population": int(population)})
        print(f"Added unique (zip code, population) pair with zip code: {zip_code} and population: {population}")

    db.commit()

    for row in locations_df.iterrows():
        city = row[1][0]
        state = row[1][1]
        lat = row[1][2]
        longg = row[1][3]

        db.execute("INSERT INTO locations (city, state, lat, long) VALUES (:city, :state, :lat, :longg)",
                    {"city": city, "state": state, "lat": float(lat), "longg": float(longg)})
        print(f"Added location: city: {city} state: {state} lat: {lat} long: {longg}")

    db.commit()

if __name__ == "__main__":
    main()