from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'TCSS.db'
db_initialized = False

def get_db():
    """Connect to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    return conn

# Create tables for the 'calendar' and 'instances' models
def create_tables():
    """Create calendar and instances tables if they do not exist."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS calendar (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            start_date TEXT,
                            end_date TEXT
                          )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS instances (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            start_id INTEGER,
                            end_id INTEGER,
                            FOREIGN KEY(start_id) REFERENCES calendar(id),
                            FOREIGN KEY(end_id) REFERENCES calendar(id)
                          )''')

# Function to load data from CSV into SQLite tables
def load_data_from_csv():
    """Load data from CSV files into the database."""
    import csv

    base_dir = os.path.dirname(__file__)  # Directory of the current script
    calendar_file = os.path.join(base_dir, 'calendar.csv')
    instances_file = os.path.join(base_dir, 'instances.csv')

    print(f"Loading calendar data from: {calendar_file}")
    print(f"Loading instances data from: {instances_file}")

    try:
        # Load calendar data
        with get_db() as conn:
            cursor = conn.cursor()
            with open(calendar_file, 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    print(f"Inserting into calendar: {row}")  # Debugging statement
                    cursor.execute('INSERT INTO calendar (start_date, end_date) VALUES (?, ?)', (row[1], row[2]))

        # Load instances data
        with open(instances_file, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                print(f"Inserting into instances: {row}")  # Debugging statement
                cursor.execute('INSERT INTO instances (name, start_id, end_id) VALUES (?, ?, ?)',
                               (row[1], row[2], row[3]))
    except FileNotFoundError as e:
        print(f"File not found: {e}")  # Specific error for file not found
    except Exception as e:
        print(f"Error loading data: {e}")  # General error handling for loading data

# Route to display lecturer's schedule
@app.route('/schedule')
def schedule_view():
    """Display the lecturer's schedule."""
    global db_initialized
    if not db_initialized:
        create_tables()
        load_data_from_csv()
        db_initialized = True

    with get_db() as conn:
        cursor = conn.cursor()
        query = '''SELECT instances.name, cal1.start_date, cal2.end_date
                   FROM instances
                   JOIN calendar AS cal1 ON instances.start_id = cal1.id
                   JOIN calendar AS cal2 ON instances.end_id = cal2.id'''
        cursor.execute(query)
        schedules = cursor.fetchall()

        print(f"Schedules fetched: {schedules}")  # Debugging statement to check the data fetched

    return render_template('schedule.html', schedules=schedules)

# Run the Flask app
if __name__ == '__main__':
    with app.test_request_context():
        print(app.url_map)  # Prints the available routes

    app.run(debug=True)
