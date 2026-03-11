"""
load_contaminantes_cloud.py
----------------------------
1. Reads seeds/outputs/fct_emisiones_energia.csv (uses a small sample to
   derive SQL column types).
2. Creates (or replaces) the table "fct_emisiones_energia" in Cloud SQL
   (PostgreSQL) with the correct data types.
3. Inserts all rows in configurable batches for memory-efficient loading.

Connection is made through the Cloud SQL Auth Proxy for a secure,
IAM-authenticated connection.

Prerequisites
-------------
1. gcloud CLI installed and authenticated:
       gcloud auth login
       gcloud auth application-default login

2. Cloud SQL Auth Proxy installed:
       # macOS (Apple Silicon)
       curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.1/cloud-sql-proxy.darwin.arm64
       chmod +x cloud-sql-proxy

       # macOS (Intel)
       curl -o cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.1/cloud-sql-proxy.darwin.amd64
       chmod +x cloud-sql-proxy

3. Python dependencies:
       pip install psycopg2-binary sqlalchemy pandas pyarrow

4. Your Cloud SQL instance must have the postgres user with the password
   stored in config/deploy.toml, and a target database must exist.
   If you don't have a database yet, create one:
       gcloud sql databases create greenlab --instance=greenlab-data-platform-sample

Usage
-----
In one terminal, start the proxy:
    ./cloud-sql-proxy consulting-data-studio:southamerica-west1:greenlab-data-platform-sample --port 5433

In another terminal, run this script:
    python scripts/data/load_contaminantes_cloud.py

Optional flags:
    --db          Database name (default: greenlab)
    --table       Target table name (default: fct_emisiones_energia)
    --batch       Rows per insert batch (default: 10000)
    --port        Proxy local port (default: 5433)
    --if-exists   'replace' (default) or 'append'
    --sample-rows Number of rows used to infer column types (default: 100)
"""

import argparse
import sys
import os
import math

# Ensure repo root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import tomllib
import pandas as pd

CSV_PATH    = "seeds/outputs/fct_emisiones_energia.csv"
CONFIG_PATH = "config/deploy.toml"

TABLE_NAME  = "fct_emisiones_energia"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config():
    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f)


def pandas_dtype_to_sql(series: pd.Series) -> str:
    """Map a pandas Series dtype to a PostgreSQL column type."""
    dtype = series.dtype
    if pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    if pd.api.types.is_float_dtype(dtype):
        return "DOUBLE PRECISION"
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATE"
    # Try to detect date strings
    if dtype == object:
        sample = series.dropna().head(10)
        try:
            pd.to_datetime(sample)
            return "DATE"
        except Exception:
            pass
        return "TEXT"
    return "TEXT"


def build_create_table_ddl(df_sample: pd.DataFrame, table: str) -> str:
    """Build a CREATE TABLE DDL from a sample DataFrame."""
    col_defs = []
    for col in df_sample.columns:
        sql_type = pandas_dtype_to_sql(df_sample[col])
        col_defs.append(f'    "{col}" {sql_type}')
    cols_sql = ",\n".join(col_defs)
    return f'CREATE TABLE "{table}" (\n{cols_sql}\n);'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Create fct_emisiones_energia table in Cloud SQL and load CSV data"
    )
    parser.add_argument("--db",           default="greenlab",              help="Database name")
    parser.add_argument("--table",        default=TABLE_NAME,              help="Target table name")
    parser.add_argument("--batch",        default=10_000, type=int,        help="Rows per insert batch")
    parser.add_argument("--port",         default=5433,   type=int,        help="Cloud SQL Proxy local port")
    parser.add_argument("--if-exists",    default="replace",               help="'replace' or 'append'")
    parser.add_argument("--sample-rows",  default=100,    type=int,        help="Rows used to infer column types")
    args = parser.parse_args()

    # --- Dependency check ---
    try:
        import psycopg2
        from psycopg2.extras import execute_values
    except ImportError:
        print("ERROR: psycopg2-binary not installed. Run:")
        print("  pip install psycopg2-binary")
        sys.exit(1)

    # --- credentials ---
    config   = load_config()
    sql_cfg  = config["cloud_sql"]
    user     = sql_cfg["user"]
    password = sql_cfg["password"]
    db       = args.db
    port     = args.port
    table    = args.table

    # -----------------------------------------------------------------------
    # 1. Sample the CSV to infer schema
    # -----------------------------------------------------------------------
    print(f"Reading sample ({args.sample_rows} rows) from {CSV_PATH} to infer schema...")
    df_sample = pd.read_csv(CSV_PATH, nrows=args.sample_rows, parse_dates=["fecha"])
    print(f"  Columns detected: {list(df_sample.columns)}")
    print()

    ddl = build_create_table_ddl(df_sample, table)
    print("DDL that will be used:")
    print(ddl)
    print()

    # -----------------------------------------------------------------------
    # 2. Connect, check for existing table, and create fresh
    # -----------------------------------------------------------------------
    print(f"Connecting to Cloud SQL via proxy (127.0.0.1:{port}/{db})...")
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=port,
        dbname=db,
        user=user,
        password=password,
    )
    conn.autocommit = False

    with conn.cursor() as cur:
        # Always check whether the table already exists and clear it first
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name = %s
            )
            """,
            (table,),
        )
        table_exists = cur.fetchone()[0]

        if table_exists:
            print(f"  Table '{table}' already exists — dropping it first...")
            cur.execute(f'DROP TABLE "{table}";')
            conn.commit()
            print(f"  Dropped '{table}'.")

        print(f"Creating table '{table}'...")
        cur.execute(ddl)
        conn.commit()
        print("  Table created successfully.\n")

    # -----------------------------------------------------------------------
    # 3. Load full CSV in batches
    # -----------------------------------------------------------------------
    print(f"Reading full CSV: {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH, parse_dates=["fecha"])
    total_rows = len(df)
    print(f"  {total_rows:,} rows × {len(df.columns)} columns")

    # Convert NaT / NaN to None so psycopg2 inserts NULL properly
    df = df.where(pd.notnull(df), None)
    # Convert date column to plain date objects
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date

    columns      = list(df.columns)
    col_list     = ", ".join(f'"{c}"' for c in columns)
    insert_sql   = f'INSERT INTO "{table}" ({col_list}) VALUES %s'
    batch_size   = args.batch
    n_batches    = math.ceil(total_rows / batch_size)

    print(f"\nInserting {total_rows:,} rows in {n_batches} batches of {batch_size:,}...")
    from psycopg2.extras import execute_values

    with conn.cursor() as cur:
        for i in range(n_batches):
            start = i * batch_size
            end   = min(start + batch_size, total_rows)
            batch = df.iloc[start:end]
            rows  = [tuple(row) for row in batch.itertuples(index=False, name=None)]

            execute_values(cur, insert_sql, rows, page_size=batch_size)
            conn.commit()
            print(f"  Batch {i + 1}/{n_batches}: rows {start + 1:,}–{end:,} committed.")

    conn.close()
    print(f"\n✅ Done — {total_rows:,} rows written to {db}.{table}")


if __name__ == "__main__":
    main()
