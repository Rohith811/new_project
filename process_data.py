import pandas as pd
import sqlite3

# Use raw string for the file path to avoid unicode escape issues
file_path = r'C:\Users\hp\OneDrive\Desktop\rohith\20210309_2020_1-4.xls'

# Read the Excel file
df = pd.read_excel(file_path, sheet_name=None, engine='xlrd')

# Combine all sheets into one DataFrame
df_combined = pd.concat(df.values(), ignore_index=True)

# Clean column names to avoid any issues
df_combined.columns = df_combined.columns.str.strip().str.upper()

# Print cleaned column names and first few rows to inspect
print("Cleaned column names:", df_combined.columns)
print("First few rows:\n", df_combined.head())



# Group by the exact column name with spaces and calculate the annual totals for oil, gas, and brine
annual_data = df_combined.groupby('API WELL  NUMBER').agg({
    'OIL': 'sum',
    'GAS': 'sum',
    'BRINE': 'sum'
}).reset_index()

# Rename columns for clarity
annual_data.columns = ['api_well_number', 'oil', 'gas', 'brine']
# Convert api_well_number to string to ensure proper handling
annual_data['api_well_number'] = annual_data['api_well_number'].astype(str)
# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('production_data.db')
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS production (
    api_well_number TEXT PRIMARY KEY,
    oil INTEGER,
    gas INTEGER,
    brine INTEGER
)
''')

# Insert data into the table
for _, row in annual_data.iterrows():
    cursor.execute('''
    INSERT OR REPLACE INTO production (api_well_number, oil, gas, brine) 
    VALUES (?, ?, ?, ?)
    ''', (row['api_well_number'], row['oil'], row['gas'], row['brine']))

cursor.execute("SELECT api_well_number, oil, gas, brine FROM production")
rows = cursor.fetchall()

if rows:
    print("Data inserted into the production table:")
    for row in rows:
        print(row)
else:
    print("No data found in the production table.")

# After data insertion, let's fetch and print the first few rows to confirm
cursor.execute("SELECT * FROM production LIMIT 5")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(row)
else:
    print("No data found in the production table.")

# Commit and close the connection
conn.commit()
conn.close()

print("Data processing and insertion into database complete.")
