import pandas as pd
import sqlite3
from pathlib import Path

def create_connection():
    """Create a database connection"""
    return sqlite3.connect('transfermarkt_data.db')

def create_tables(conn):
    """Create tables with appropriate schema"""
    # Players table
    players_schema = """
    CREATE TABLE IF NOT EXISTS players (
        player_id TEXT PRIMARY KEY,
        name TEXT,
        current_club_id TEXT,
        -- Add other columns as needed
        FOREIGN KEY (current_club_id) REFERENCES clubs (club_id)
    );
    """
    
    # Player valuations table
    valuations_schema = """
    CREATE TABLE IF NOT EXISTS player_valuations (
        player_id TEXT,
        date DATE,
        market_value_in_eur DECIMAL,
        -- Add other columns as needed
        FOREIGN KEY (player_id) REFERENCES players (player_id)
    );
    """
    
    # Add more table schemas as needed
    
    conn.execute(players_schema)
    conn.execute(valuations_schema)
    conn.commit()

def load_data():
    conn = create_connection()
    
    # List of CSV files and their corresponding table names
    tables = {
        'players': 'data/players.csv',
        'player_valuations': 'data/player_valuations.csv',
        'appearances': 'data/appearances.csv',
        'clubs': 'data/clubs.csv',
        'competitions': 'data/competitions.csv',
        'games': 'data/games.csv'
    }
    
    for table_name, file_path in tables.items():
        print(f"Loading {table_name}...")
        
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Load to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        # Verify the data
        count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", conn)
        print(f"Loaded {count['count'].iloc[0]} rows to {table_name}")
    
    conn.close()

def verify_data():
    """Run some basic queries to verify the data"""
    conn = create_connection()
    
    # Example queries
    queries = {
        "Total players": "SELECT COUNT(*) FROM players",
        "Players with valuations": """
            SELECT COUNT(DISTINCT p.player_id) 
            FROM players p
            JOIN player_valuations pv ON p.player_id = pv.player_id
        """,
        "Sample player data": """
            SELECT p.name, pv.market_value_in_eur, pv.date
            FROM players p
            JOIN player_valuations pv ON p.player_id = pv.player_id
            LIMIT 5
        """
    }
    
    for description, query in queries.items():
        print(f"\n{description}:")
        result = pd.read_sql(query, conn)
        print(result)
    
    conn.close()

if __name__ == "__main__":
    load_data()
    verify_data()