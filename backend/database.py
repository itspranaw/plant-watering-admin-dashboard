import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()  # Load variables from .env file if available

# Retrieve database connection details from environment variables or use defaults
MYSQL_USER = os.getenv("MYSQL_USER", "pranaw")
MYSQL_PASSWORD_RAW = os.getenv("MYSQL_PASSWORD", "pasS@123")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_DB = os.getenv("MYSQL_DB", "plant_db")

# URL-encode the password to handle special characters like '@'
MYSQL_PASSWORD = quote_plus(MYSQL_PASSWORD_RAW)

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
