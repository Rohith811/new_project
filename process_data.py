import pandas as pd
import sqlite3

def process_data(file_path):
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
    annual_data['api_well_number'] = annual_data['api_well_number'].astype(str)
    
    # Connect to SQLite database (or create it if it doesn't exist)
    with sqlite3.connect('production_data.db') as conn:
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
        
        # Insert data into the table in bulk
        data_tuples = [tuple(x) for x in annual_data.to_numpy()]
        cursor.executemany('''
        INSERT OR REPLACE INTO production (api_well_number, oil, gas, brine) 
        VALUES (?, ?, ?, ?)
        ''', data_tuples)
        
        # Commit changes
        conn.commit()
        
    print("Data processing and insertion into database complete.")

if __name__ == '__main__':
    file_path = r'C:\Users\hp\OneDrive\Desktop\rohith\20210309_2020_1-4.xls'
    process_data(file_path)
