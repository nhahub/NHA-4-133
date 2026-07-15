# ==============================================================================
# Automated Post-Hospital Patient Monitoring System
# Script   : load_to_sql.py
# Purpose  : Loads the cleaned patient vitals dataset into the Azure SQL
#            Database table [dbo].[patient_vitals] using batch inserts.
# Author   : Graduation Project Team
# Date     : 2026-07-10
# Usage    : python src/database/load_to_sql.py
# ==============================================================================

import os
import sys
from urllib.parse import quote_plus
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

# ==============================================================================
# STEP 1: Load environment variables from the .env file.
# python-dotenv reads key=value pairs from .env into os.environ so that
# credentials are never hardcoded in source code.
# ==============================================================================
load_dotenv()

# ==============================================================================
# STEP 2: Read and validate the required database configuration variables.
# The script terminates early with a clear message if any variable is missing,
# preventing a confusing connection error later.
# ==============================================================================
AZURE_SQL_SERVER   = os.getenv("AZURE_SQL_SERVER")
AZURE_SQL_DATABASE = os.getenv("AZURE_SQL_DATABASE")
AZURE_SQL_USERNAME = os.getenv("AZURE_SQL_USERNAME")
AZURE_SQL_PASSWORD = os.getenv("AZURE_SQL_PASSWORD")

missing = [
    name for name, value in {
        "AZURE_SQL_SERVER":   AZURE_SQL_SERVER,
        "AZURE_SQL_DATABASE": AZURE_SQL_DATABASE,
        "AZURE_SQL_USERNAME": AZURE_SQL_USERNAME,
        "AZURE_SQL_PASSWORD": AZURE_SQL_PASSWORD,
    }.items()
    if not value
]

if missing:
    print(f"[ERROR] The following required environment variables are not set: {', '.join(missing)}")
    print("        Please copy .env.example to .env and fill in your credentials.")
    sys.exit(1)

# ==============================================================================
# STEP 3: Define file paths.
# Paths are resolved relative to this script's location so the script can be
# run from any working directory.
# ==============================================================================
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT    = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
CSV_PATH        = os.path.join(PROJECT_ROOT, "data", "processed", "patient_vitals_clean.csv")
TARGET_TABLE    = "patient_vitals"
BATCH_SIZE      = 10_000

# ==============================================================================
# STEP 4: Load the cleaned CSV dataset into a Pandas DataFrame.
# The script raises a descriptive FileNotFoundError if the processed file does
# not exist, guiding the user to run clean_data.py first.
# ==============================================================================
print(f"Loading cleaned dataset from: {CSV_PATH}")

try:
    df = pd.read_csv(CSV_PATH, parse_dates=["timestamp"])
except FileNotFoundError:
    print(f"[ERROR] Cleaned dataset not found at: {CSV_PATH}")
    print("        Please run 'python src/cleaning/clean_data.py' to generate it first.")
    sys.exit(1)

print(f"Dataset loaded successfully. Shape: {df.shape[0]:,} rows x {df.shape[1]} columns.")

# ==============================================================================
# STEP 5: Rename columns to match the SQL table schema.
# The cleaned CSV uses slightly different column names than the target table:
#   CSV column name             -> SQL table column name
#   'timestamp'                 -> 'measured_at'
#   'systolic_blood_pressure'   -> 'systolic_bp'
#   'diastolic_blood_pressure'  -> 'diastolic_bp'
# This rename is applied in-memory; no files are modified.
# ==============================================================================
print("Aligning DataFrame column names with the SQL table schema...")

df = df.rename(columns={
    "timestamp":                "measured_at",
    "systolic_blood_pressure":  "systolic_bp",
    "diastolic_blood_pressure": "diastolic_bp",
})

# The 'ingested_at' column is intentionally excluded here.
# It is auto-populated by the DEFAULT SYSUTCDATETIME() constraint
# defined in create_patient_vitals.sql.

print("Column alignment complete.")

# ==============================================================================
# STEP 6: Build the SQLAlchemy connection string and create the database engine.
# - ODBC Driver 18 is the recommended driver for Azure SQL Database.
# - TrustServerCertificate=yes is included for local/dev environments.
# - fast_executemany=True on the pyodbc creator significantly increases
#   bulk insert throughput by reducing Python-to-driver round trips.
# ==============================================================================
print("Establishing connection to Azure SQL Database...")

CONNECTION_STRING = (
    f"mssql+pyodbc://{quote_plus(AZURE_SQL_USERNAME)}:{quote_plus(AZURE_SQL_PASSWORD)}"
    f"@{AZURE_SQL_SERVER}/{AZURE_SQL_DATABASE}"
    f"?driver=ODBC+Driver+18+for+SQL+Server"
    f"&TrustServerCertificate=yes"
)

try:
    engine = create_engine(
        CONNECTION_STRING,
        connect_args={"fast_executemany": True}
    )

    # Verify the connection is live before attempting to load 200k rows.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    print("Database connection established successfully.")

except OperationalError as e:
    print(f"[ERROR] Database connection failed.")
    print(f"        Details: {e}")
    print("        Please verify AZURE_SQL_SERVER, AZURE_SQL_USERNAME, and AZURE_SQL_PASSWORD in your .env file.")
    sys.exit(1)

# ==============================================================================
# STEP 7: Insert the data into the SQL table in batches.
# - The DataFrame is sliced into chunks of BATCH_SIZE rows.
# - Each chunk is appended to the existing table using pandas to_sql().
# - if_exists='append' ensures the pre-created table is not dropped or
#   recreated by this script.
# - method='multi' batches multiple rows per INSERT statement for efficiency.
# - Progress is printed after every batch to provide visibility on long runs.
# ==============================================================================
print(f"\nStarting batch insert into [{TARGET_TABLE}] (batch size: {BATCH_SIZE:,} rows)...")
print("-" * 60)

total_rows     = len(df)
rows_inserted  = 0

try:
    for start in range(0, total_rows, BATCH_SIZE):
        batch = df.iloc[start : start + BATCH_SIZE]

        batch.to_sql(
            name        = TARGET_TABLE,
            con         = engine,
            schema      = "dbo",
            if_exists   = "append",
            index       = False,
            method      = "multi",
        )

        rows_inserted += len(batch)
        print(f"Inserted {rows_inserted:,} rows...")

except SQLAlchemyError as e:
    print(f"\n[ERROR] A SQL execution error occurred after inserting {rows_inserted:,} rows.")
    print(f"        Details: {e}")
    print("        Please verify the table schema matches [dbo].[patient_vitals] defined in sql/create_patient_vitals.sql.")
    sys.exit(1)

except Exception as e:
    print(f"\n[ERROR] An unexpected error occurred after inserting {rows_inserted:,} rows.")
    print(f"        Details: {e}")
    sys.exit(1)

# ==============================================================================
# STEP 8: Print the final success message and a brief summary.
# ==============================================================================
print("-" * 60)
print(f"Data successfully loaded into {TARGET_TABLE}.")
print(f"Total rows inserted: {rows_inserted:,}")
