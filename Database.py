import sqlite3
import csv
import os
import re
import shutil
### PATH AND DIRECTORY SETUP ###
### Get the directory of the script ###
script_directory = os.path.dirname(os.path.abspath(__file__))
subdirectory = "Data"
db_dir = "db"
backup_dir="backup"
### Define the directory path where you want to save the database ###
backup_directory = os.path.join(script_directory, backup_dir, "Backup_DB_Immo.db")
db_path = os.path.join(script_directory, db_dir, "Database_Immo.db")
#### In the vast cosmos of directories, we create if we don't find ####
if not os.path.exists(backup_directory):
    os.makedirs(backup_directory)
### CREATING LIST WITH CITIES ###
directory_path = os.path.join(script_directory, subdirectory)
files = os.listdir(directory_path)
cities = []
expected_headers = [
    "Code", "Prijs", "Adres", "Stad", "Type", "Bouwjaar", "EPC", "Woonopp", 
    "Slaapkamers", "Badkamers", "Grondopp", "Bebouwing", "Garages", "Tuin", 
    "Dagen", "Link", "Handelsopp", "First", "Last", "Scraped"
]
### I. Process each file like a fleeting moment in existence ###
for file in files:
    match = re.match(r"Final_File_(.+)\.csv", file)
    if match:
        cities.append(match.group(1))
cities.append("FULL")
### FUNCTION DEFINITIONS ###
### I.I Clean and purify data, much like life's imperfections ###
def clean_value(value, retain_decimal=False):
    if retain_decimal:
        cleaned_value = re.sub('[^0-9.]', '', value)
        try:
            return float(cleaned_value)
        except ValueError:
            return None
    else:
        cleaned_value = re.sub('[^0-9]', '', value)
        return int(cleaned_value) if cleaned_value and int(cleaned_value) != 0 else None
### I.II Evolution of the table, evolving and changing, as we do ###
def process_table(table_name, cursor):
    ### I.II.I Add columns if they don't exist, life's surprising additions ###
    if not column_exists(table_name, "P_Change", cursor):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_Change REAL")
    #### Embracing life's redundancies, repetition is the essence of existence ####
    ### I.II.II Calculate price change for duplicates with differing 'Prijs' values ###
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
        AND P_Change IS NULL
    """)
    ### I.II.III Calculate price change for duplicates with differing 'Prijs' values ###
	
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


    #### Cleansing the past, leaving behind only what's necessary ####
    cursor.execute(f"""
        DELETE FROM {table_name}
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM {table_name}
            GROUP BY Code, Prijs
            HAVING COUNT(*) = 1 OR Dagen = MAX(Dagen)
        )
    """)
### I.III In a world of constant updates, adapt or become obsolete ###
def update_tables(table_name, cursor):
    ### I.III.I Ensure new attributes find their place in our table's universe ###
    if not column_exists(table_name, "P_WOON", cursor):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_WOON REAL")
    if not column_exists(table_name, "P_GROND", cursor):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN P_GROND REAL")
    
    ### I.III.II Adjust to the times, change is the only constant ###
    # Update 'P/WOON' column values with added WHERE clause
    cursor.execute(f"""
        UPDATE {table_name}
        SET P_WOON = CASE 
            WHEN Woonopp IS NOT NULL AND Woonopp != 0 THEN Prijs / Woonopp
            ELSE NULL
        END
        WHERE P_WOON IS NULL
    """)
	
    # Update 'P/GROND' column values with added WHERE clause
    cursor.execute(f"""
        UPDATE {table_name}
        SET P_GROND = CASE 
            WHEN Grondopp IS NOT NULL AND Grondopp != 0 THEN Prijs / Grondopp
            ELSE NULL
        END
        WHERE P_GROND IS NULL
    """)
### I.IV Our database's mirror, reflecting on its own structure ###
def column_exists(table_name, column_name, cursor):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

### I.V Fixing the fragments of memory we access ###
#def fix_csv_headers(csv_file_path, expected_headers):  # Code omitted

### I.VI Evolution demands we modify when necessary ###
def modify_csv_if_needed(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    headers = rows[0]

    # Check if there are extra columns beyond the expected ones.
    if headers != expected_headers:
        # Index of "Scraped" column + 1
        cut_off_index = headers.index("Scraped") + 1
        
        # Rewrite the CSV with only the required columns
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row[:cut_off_index])  
### II. The existential journey of data through CSV to SQL ###
cols_to_clean = ['EPC', 'Bouwjaar', 'Slaapkamers', 'Badkamers', 'Garages', 'Handelsopp', 'Woonopp']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

### II.I Each city is a chapter in our database's story ###
for city in cities:
    table_name = city
    if city == 'FULL':
        csv_file_path = r'C:\Users\Ivan\Desktop\Python\Immo_scraper\Data\Final_File.csv'
    else:
        csv_file_path = r'C:\Users\Ivan\Desktop\Python\Immo_scraper\Data\Final_File_' + city + '.csv'
    
    ### II.I.I Rewriting memories before diving deep ###
    #fix_csv_headers(csv_file_path, expected_headers)
    modify_csv_if_needed(csv_file_path)
    
    #### Much like our own existence, sometimes we need a structure to function ####
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

    #### Every piece of data, a memory, etched into our universe ####
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            # Clean specified columns
            row = {k: clean_value(v, k == 'Woonopp') if k in cols_to_clean else v for k, v in row.items()}            
            placeholders = ', '.join(['?'] * len(row))
            columns = ', '.join([f'"{k}"' for k in row.keys()])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(row.values()))

    conn.commit()

    process_table(city, cursor)
    update_tables(city, cursor)
### III. A chapter ends, another begins, yet the story remains eternal ###
conn.commit()
conn.close()
#### As with life, always make a backup. Memories are precious ####
shutil.copy2(db_path, backup_directory)