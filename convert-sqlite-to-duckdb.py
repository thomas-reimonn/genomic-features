import sqlite3

import duckdb


def copy_sqlite_to_duckdb(sqlite_path, duckdb_path):
    """Copy all tables from a SQLite database to a DuckDB database."""
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect(sqlite_path)
    cursor = sqlite_conn.cursor()

    # Retrieve list of all tables in SQLite database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Connect to DuckDB
    duckdb_conn = duckdb.connect(duckdb_path)

    # Attach SQLite database to DuckDB
    duckdb_conn.execute(f"ATTACH DATABASE '{sqlite_path}' AS sqlite_db")

    # Copy each table from SQLite to DuckDB
    for table_name in tables:
        table_name = table_name[0]  # Unpack tuple
        print(f"Copying {table_name}...")
        duckdb_conn.execute(
            f"CREATE TABLE {table_name} AS SELECT * FROM sqlite_db.{table_name};"
        )

    print("All tables copied successfully.")

    # Close connections
    sqlite_conn.close()
    duckdb_conn.close()


# Path to your SQLite and DuckDB databases
sqlite_path = "/Users/thomas/Library/Caches/genomic-features/9497c13b06fa5d305fb592a9601563a7-EnsDb.Hsapiens.v108.sqlite"
duckdb_path = "/Users/thomas/Library/Caches/genomic-features/9497c13b06fa5d305fb592a9601563a7-EnsDb.Hsapiens.v108.duckdb"

# Execute the function
copy_sqlite_to_duckdb(sqlite_path, duckdb_path)
