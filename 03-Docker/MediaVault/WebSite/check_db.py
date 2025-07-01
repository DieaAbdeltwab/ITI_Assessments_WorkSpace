import sqlite3

def check_tables():
    conn = sqlite3.connect('db/anime.db')
    cursor = conn.cursor()
    
    # Get list of tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:")
    for table in tables:
        print(f"- {table[0]}")
        
        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print(f"  Columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
            
        # Show sample data for genre column if it exists
        cursor.execute(f"SELECT * FROM {table[0]} LIMIT 1;")
        sample = cursor.fetchone()
        if sample:
            print(f"  Sample data: {sample}")
        print()
    
    conn.close()

if __name__ == "__main__":
    check_tables()
