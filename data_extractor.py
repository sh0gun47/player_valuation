import pandas as pd
import os
import sqlite3
from pathlib import Path

def create_connection():
    """Create a connection to the database"""
    conn = sqlite3.connect('football_data.db')
    return conn

def load_data_to_sqlite():
    conn = create_connection()

    # List of datasets to process
    datasets = [
        'players',
        'player_valuations',
        'appearances',
        'clubs',
        'club_games',
        'competitions',
        'game_events',
        'game_lineups',
        'games',
        'player_valuations',
        'transfers'
    ]

    for dataset in datasets:
        print(f"Processing {dataset} dataset...")

        # Read CSV
        df = pd.read_csv(f'data/{dataset}.csv')

        # Load data to SQLite
        df.to_sql(dataset, conn, if_exists='replace', index=False)

        # Verify the data
        count = pd.read_sql(f"SELECT COUNT(*) FROM {dataset}", conn).iloc[0,0]
        print(f"Loaded {count} rows into {dataset} table")

    conn.close()

def example_query():
    """Example of how to query the data"""
    conn = create_connection()
    
    query = """
    SELECT * FROM players 
    LIMIT 5
    """
    
    result = pd.read_sql(query, conn)
    print("\nSample Query Result:")
    print(result)
    
    conn.close()

if __name__ == "__main__":
    load_data_to_sqlite()
    example_query()