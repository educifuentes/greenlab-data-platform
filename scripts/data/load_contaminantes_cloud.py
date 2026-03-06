"""
load_contaminantes_cloud.py
----------------------------
Loads seeds/outputs/fct_emisiones_energia.parquet into Cloud SQL (PostgreSQL)
using the Cloud SQL Auth Proxy for a secure, IAM-authenticated connection.

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
    --db      Database name (default: greenlab)
    --table   Target table name (default: fct_emisiones_energia)
    --batch   Rows per insert batch (default: 10000)
    --port    Proxy local port (default: 5433)
    --if-exists  'replace' (default) or 'append'
"""

import argparse
import sys
import os

# Ensure repo root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import tomllib
import pandas as pd

PARQUET_PATH = "seeds/outputs/fct_emisiones_energia.parquet"
CONFIG_PATH  = "config/deploy.toml"


def load_config():
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    return config


def main():
    parser = argparse.ArgumentParser(description="Load fct_emisiones_energia parquet into Cloud SQL")
    parser.add_argument("--db",         default="greenlab",                help="Database name")
    parser.add_argument("--table",      default="fct_emisiones_energia",   help="Target table name")
    parser.add_argument("--batch",      default=10_000, type=int,          help="Rows per batch")
    parser.add_argument("--port",       default=5433,   type=int,          help="Cloud SQL Proxy local port")
    parser.add_argument("--if-exists",  default="replace",                 help="'replace' or 'append'")
    args = parser.parse_args()

    # --- Dependencies check ---
    try:
        from sqlalchemy import create_engine
    except ImportError:
        print("ERROR: sqlalchemy not installed. Run:")
        print("  pip install psycopg2-binary sqlalchemy pandas pyarrow")
        sys.exit(1)

    # --- Load credentials ---
    config = load_config()
    sql_cfg = config["cloud_sql"]
    user     = sql_cfg["user"]
    password = sql_cfg["password"]
    db       = args.db
    port     = args.port

    connection_url = f"postgresql+psycopg2://{user}:{password}@127.0.0.1:{port}/{db}"

    # --- Load parquet ---
    print(f"Reading {PARQUET_PATH}...")
    df = pd.read_parquet(PARQUET_PATH)
    print(f"  {len(df):,} rows × {len(df.columns)} columns")

    # --- Upload ---
    print(f"\nConnecting to Cloud SQL via proxy (127.0.0.1:{port})...")
    engine = create_engine(connection_url)

    print(f"Writing to table '{args.table}' (if_exists='{args.if_exists}', batch={args.batch:,})...")
    df.to_sql(
        name=args.table,
        con=engine,
        if_exists=args.if_exists,
        index=False,
        chunksize=args.batch,
        method="multi",
    )

    print(f"\n✅ Done — {len(df):,} rows written to {db}.{args.table}")


if __name__ == "__main__":
    main()
