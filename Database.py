import sqlite3
import csv
import os
import re
import shutil

###Get the directory of the script##
script_directory = os.path.dirname(os.path.abspath(__file__))
subdirectory = "Data"
db_dir = "db"
backup_dir="backup"

# Define the directory path where you want to save the database
backup_directory = os.path.join(script_directory, backup_dir, "Backup_DB_Immo.db")
db_path = os.path.join(script_directory, db_dir, "Database_Immo.db")

# Create backup the directory if it doesn't exist
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)

#CREATING LIST WITH CITIES#
directory_path = os.path.join(script_directory, subdirectory)
files = os.listdir(directory_path)

cities = []
#CREATING LIST WITH CITIES#

for file in files:
    # Match files that start with "Final_File_" and end with ".csv"
    match = re.match(r"Final_File_(.+)\.csv", file)
    if match:
        cities.append(match.group(1))

### All the defs ###
def clean_value(value):
    """Clean values for specified columns."""
    cleaned_value = re.sub('[^0-9]', '', value)
    return float(cleaned_value) if cleaned_value and int(cleaned_value) != 0 else None

def process_table(table_name, cursor):
    # Add 'P.Change' column
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_Change REAL")

    # Calculate price change for duplicates with differing 'Prijs' values
    cursor.execute(f"""
        UPDATE {table_name}
        SET P_Change = (
            SELECT CASE 
                       WHEN Prijs = MAX(Prijs) THEN Prijs - MIN(Prijs)
                       ELSE MIN(Prijs) - Prijs
                   END
            FROM {table_name} AS innerTable
            WHERE innerTable.Code = {table_name}.Code
            GROUP BY innerTable.Code
            HAVING COUNT(*) > 1 AND MIN(Prijs) <> MAX(Prijs)
        )
        WHERE Code IN (
            SELECT Code FROM {table_name} GROUP BY Code HAVING COUNT(*) > 1
        )
    """)

    # Delete duplicates with the same 'Prijs' but keep the one with the highest 'Dagen'
    cursor.execute(f"""
        DELETE FROM {table_name}
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM {table_name}
            GROUP BY Code, Prijs
            HAVING COUNT(*) = 1 OR Dagen = MAX(Dagen)
        )
    """)

    # Delete rows where 'Code' is empty or NULL
    cursor.execute(f"DELETE FROM {table_name} WHERE Code IS NULL OR Code = ''")

def update_tables(table_name, cursor):
    # Add 'P/WOON' and 'P/GROND' columns
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_WOON REAL")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_GROND REAL")

    # Update 'P/WOON' column values
    cursor.execute(f"""
        UPDATE {table_name}
        SET P_WOON = CASE 
            WHEN Woonopp IS NOT NULL AND Woonopp != 0 THEN Prijs / Woonopp
            ELSE NULL
        END
    """)

    # Update 'P/GROND' column values
    cursor.execute(f"""
        UPDATE {table_name}
        SET P_GROND = CASE 
            WHEN Grondopp IS NOT NULL AND Grondopp != 0 THEN Prijs / Grondopp
            ELSE NULL
        END
    """)


# CSV processing and data insertion
cols_to_clean = ['EPC', 'Bouwjaar', 'Slaapkamers', 'Badkamers', 'Garages', 'Handelsopp', 'Woonopp']

cities = ['Antwerpen', 'Brussel', 'Erembodegem', 'Gent', 'FULL']  # Added 'FULL' to the cities list

# Database setup
#conn = sqlite3.connect('properties.db')
#cursor = conn.cursor()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# For each city, process the corresponding CSV file and insert data into the corresponding table
for city in cities:
    table_name = city
    if city == 'FULL':
        csv_file_path = r'C:\Users\Ivan\Desktop\Python\Immo_scraper\Data\Final_File.csv'
    else:
        csv_file_path = r'C:\Users\Ivan\Desktop\Python\Immo_scraper\Data\Final_File_' + city + '.csv'
    
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        Code TEXT, Prijs REAL, Adres TEXT, Stad TEXT, Type TEXT, 
        Bouwjaar REAL, EPC REAL, Woonopp REAL, Slaapkamers REAL, 
        Badkamers REAL, Grondopp REAL, Bebouwing TEXT, Garages TEXT,
        Tuin TEXT, Dagen REAL, Link TEXT, Handelsopp REAL, 
        First TIMESTAMP, Last TIMESTAMP, Scraped TIMESTAMP
    );
    """)
    conn.commit()

    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Clean specified columns
            row = {k: clean_value(v) if k in cols_to_clean else v for k, v in row.items()}
            placeholders = ', '.join(['?'] * len(row))
            columns = ', '.join([f'"{k}"' for k in row.keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(row.values()))

    conn.commit()

for city in cities:
    process_table(city, cursor)
    update_tables(city, cursor)

# Commit changes
conn.commit()
# Close the connection
conn.close()

shutil.copy2(db_path, backup_directory)