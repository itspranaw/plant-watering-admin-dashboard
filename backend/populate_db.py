import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env if available
load_dotenv()

# Database credentials
MYSQL_USER = os.getenv("MYSQL_USER", "pranaw")
MYSQL_PASSWORD_RAW = os.getenv("MYSQL_PASSWORD", "pasS@123")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "plant_db")

# URL-encode the password to handle special characters like '@'
MYSQL_PASSWORD = quote_plus(MYSQL_PASSWORD_RAW)

# Build the connection URL
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def populate_database(csv_file_path: str):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        print(f"CSV file '{csv_file_path}' loaded successfully.")
        print("CSV columns:", df.columns.tolist())
        
        # Rename CSV columns to match the model defined in models.py:
        #   - 'idMiscellaneous' will become 'id'
        #   - 'subject' will become 'name'
        #   - 'reading' will become 'reading_string'
        df = df.rename(columns={
            'idMiscellaneous': 'id',
            'subject': 'name',
            'reading': 'reading_string'
        })
        
        # If your CSV does not have a 'user_id', add one with a default value (e.g., 0)
        if 'user_id' not in df.columns:
            df['user_id'] = 0
        
        # Drop any extra columns not used by your model (for example, 'createdat')
        if 'createdat' in df.columns:
            df = df.drop(columns=['createdat'])
        
        # Use if_exists="replace" to drop any existing table and create a new one with the correct schema.
        df.to_sql("data_history1", con=engine, if_exists="replace", index=False)
        print("Data inserted successfully into 'data_history1' table with the updated schema.")
    except SQLAlchemyError as db_err:
        print("Database error occurred:", db_err)
    except Exception as err:
        print("An error occurred:", err)

if __name__ == "__main__":
    csv_file = "data_history1.csv"  # Adjust the path if needed
    populate_database(csv_file)
