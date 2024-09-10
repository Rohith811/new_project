
Ohio Well Production Data API
------------------------------------
This project processes quarterly oil, gas, and brine production data from Ohio's wells and calculates annual totals for each well. The data is then stored in an SQLite database, and a Flask API is provided to access the data via HTTP GET requests.

::Features::
Data Processing: Aggregates quarterly data into annual totals for oil, gas, and brine based on API well numbers.
Database: Stores processed data in a local SQLite database (production_data.db).
REST API: Provides an API endpoint to query the annual production data by API well number.

::Requirements::
Python 3.x
Required Python libraries:
pandas
sqlite3 (included with Python)
Flask
xlrd (for reading .xls Excel files)

::Working::
Data Processing:
The process_data.py script reads the quarterly production data from an Excel file.
It sums the quarterly values to calculate annual totals for each well's oil, gas, and brine production.
The calculated data is stored in an SQLite database (production_data.db).

API:
The main.py script sets up a Flask server that listens on port 8080.
It provides an API endpoint to retrieve the annual production data for a specific well based on its API well number.
