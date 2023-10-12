import sqlite3
import os
from geopy.geocoders import Nominatim
import time

### I. Getting Latitude and Longitude from Address ###
def get_lat_lon_osm(address):
    #### Some days I can't find my keys; today, I'm looking for an address. ####
    geolocator = Nominatim(user_agent="kaupfmann@gmail.com")
    try:
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        #### If the geocoder can't find the address, does it even exist? And where are my keys? ####
        print(f"Error geocoding {address}: {e}")
        return None, None

### II. Checking Column Existence in a Database Table ###
def columns_exist(cursor, table_name, columns):
    #### Checking if columns exist. Next up: checking if I still exist after my last coffee. ####
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [col[1] for col in cursor.fetchall()]
    return all(col in existing_columns for col in columns)

### III. Updating the Database with Latitude and Longitude ###
def update_database_with_lat_lon_osm(db_path):
    #### Life's a journey. So is updating a database, but with fewer existential crises. ####
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    ### III.I Checking and Creating Latitude and Longitude Columns ###
    if not columns_exist(cursor, "Full", ["latitude", "longitude"]):
        cursor.execute("ALTER TABLE Full ADD COLUMN latitude REAL")
        cursor.execute("ALTER TABLE Full ADD COLUMN longitude REAL")

    ### III.II Fetching Addresses and Updating ###
    cursor.execute("""
        SELECT rowid, Adres, Stad 
        FROM Full
        WHERE latitude IS NULL AND longitude IS NULL AND Code NOT IN (SELECT DISTINCT Code FROM Full WHERE latitude IS NOT NULL AND longitude IS NOT NULL)
    """)
    rows = cursor.fetchall()

    total_addresses = len(rows)
    print(f"Total addresses to process: {total_addresses}")

    for idx, row in enumerate(rows, start=1):
        rowid, address, city = row
        print(f"Processing address {idx} out of {total_addresses}")

        #### Address without a name? Like a morning without coffee: unimaginable! ####
        if not address:
            continue

        full_address = f"{address}, {city}"
        lat, lon = get_lat_lon_osm(full_address)

        if lat and lon:
            cursor.execute("UPDATE Full SET latitude=?, longitude=? WHERE rowid=?", (lat, lon, rowid))
            conn.commit()

        time.sleep(1.5)

    conn.close()
    
### IV. The Main Act - The Path to Our Database ###
#### Every database is like a good joke: it's all about the execution. ####
script_directory = os.path.dirname(os.path.realpath(__file__))
db_dir = "db"
db_path = os.path.join(script_directory, db_dir, "Database_Immo.db")

update_database_with_lat_lon_osm(db_path)
