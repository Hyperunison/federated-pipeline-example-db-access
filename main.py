# File: query_table.py

import os
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

DSN_FILE = '/data/dsn.txt'
OUTPUT_FILE = '/data/result.txt'
QUERY = "SELECT version(), now()"

def read_dsn(path):
    if not os.path.exists(path):
        logging.error(f"DSN file not found at {path}")
        raise FileNotFoundError(f"DSN file not found at {path}")

    with open(path, 'r') as f:
        dsn = f.read().strip()
        if not dsn:
            logging.error("DSN file is empty.")
            raise ValueError("DSN file is empty.")
        logging.info("DSN read successfully.")
        return dsn

def connect_and_query(dsn):
    try:
        engine = create_engine(dsn, future=True)
        with engine.connect() as conn:
            logging.info("Database connection successful.")
            result = conn.execute(text(QUERY))
            rows = result.fetchall()
            columns = result.keys()
            logging.info(f"Query executed successfully. Retrieved {len(rows)} rows.")
            return columns, rows
    except SQLAlchemyError as e:
        logging.exception("SQLAlchemy error occurred.")
        raise
    except Exception as e:
        logging.exception("Unexpected error during DB connection or query.")
        raise

def write_results(columns, rows, output_path):
    try:
        with open(output_path, 'w') as f:
            f.write('\t'.join(columns) + '\n')
            for row in rows:
                f.write('\t'.join(str(val) if val is not None else '' for val in row) + '\n')
        logging.info(f"Results written to {output_path}.")
    except Exception as e:
        logging.exception("Failed to write results to file.")
        raise

def main():
    try:
        dsn = read_dsn(DSN_FILE)
        columns, rows = connect_and_query(dsn)
        write_results(columns, rows, OUTPUT_FILE)
        logging.info("Script completed successfully.")
    except Exception as e:
        logging.error("Script failed. See above logs for details.")

if __name__ == '__main__':
    main()
