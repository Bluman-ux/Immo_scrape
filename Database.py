import pandas as pd
import sqlite3
import os

###Get the directory of the script##
script_directory = os.path.dirname(os.path.abspath(__file__))
subdirectory = "Data"
db_dir = "db"


# Path to your SQLite database and CSV
db_path = os.path.join(script_directory, db_dir,f'immo_data.db')
csv_path = os.path.join(script_directory, subdirectory, f"Final_File.csv")

def preprocess_dataframe(df):
    # Columns to be cleaned for numbers only
    clean_num_columns = [
        "Prijs", "Bouwjaar", "EPC", "Woonopp.", "Slaapkamers", 
        "Badkamers", "Grondopp.", "Dagen", "Handelsopp."
    ]

    # Clean these columns to retain only numeric values
    for col in clean_num_columns:
        df[col] = df[col].astype(str).str.extract('(\d+)').astype(float)

    # Date columns
    date_columns = ["First", "Last", "Scraped"]
    for col in date_columns:
        df[col] = pd.to_datetime(df[col])
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Setting general float columns to string
    string_columns = ["Code", "Adres", "Stad", "Type", "Bebouwing", "Garages", "Tuin", "Link"]
    for col in string_columns:
        df[col] = df[col].astype(str)
    
    return df

# Read the new CSV data and preprocess it
new_data = pd.read_csv(csv_path)
new_data = preprocess_dataframe(new_data)

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Check if 'properties' table exists in the database
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='properties';").fetchall()

if tables:
    # If the table exists, read its data into a DataFrame
    old_data = pd.read_sql("SELECT * FROM properties", conn)
    # Concatenate old and new data
    combined_data = pd.concat([old_data, new_data], ignore_index=True)
else:
    combined_data = new_data

# Handle duplicates and 'P.Change' column as before
duplicate_groups = combined_data[combined_data.duplicated(subset='Code', keep=False)].groupby('Code')
combined_data['P.Change'] = None
for code, group in duplicate_groups:
    if group['Prijs'].nunique() > 1:
        min_days_price = group.loc[group['Dagen'].idxmin(), 'Prijs']
        combined_data.loc[group.index, 'P.Change'] = group['Prijs'] - min_days_price

# Handle NaN values in the 'P.Change' column
combined_data['P.Change'].fillna(0, inplace=True)

# Save the combined and processed data back to the 'properties' table
combined_data.to_sql('properties', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
