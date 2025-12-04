import sqlite3
import os
from faker import Faker

fake = Faker("sv_SE")  # svenska namn

def init_database(num_users=5):
    """Initialize the database and create user table, then seed with Faker users."""
    db_path = os.getenv('DATABASE_PATH','data/test_users.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect (db_path)
    cursor = conn.cursor()

    # Create user table
    cursor.execute(''' 
                   CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   name TEXT NOT NULL, 
                   email TEXT NOT NULL 
                )
    ''')
    
    # Check if users already exist
    cursor.execute ('SELECT COUNT (*) FROM users')
    count = cursor.fetchone()[0]

    if count == 0:
        # Skapa syntetiska användare med Faker
        fake_users = [(fake.name(), fake.email()) for _ in range(5)]
        cursor.executemany('INSERT INTO users (name, email) VALUES (?, ?)', fake_users)
        print("Database initialized with synthetic users (GDPR compliant)")

    else:
        print(f"Database already contains {count} users")

    conn.commit()
    conn.close()

def display_users():
    """Display all users in the database"""
    db_path = os.getenv('DATABASE_PATH','data/test_users.db')
    conn = sqlite3.connect (db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    print("\nCurrent users in database:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
        
    
    conn.close()

def clear_test_data():
    """GDPR Action 1: Clear all test data"""
    db_path = os.getenv('DATABASE_PATH','data/test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tar bort alla användare
    cursor.execute('DELETE FROM users')

    # Nollställ autoincrement
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="users"')

    conn.commit()
    conn.close()
    print("All test data has been cleared (GDPR compliant)")

def anonymize_data():
    """GDPR Action 2: Anonymize user data"""
    db_path = os.getenv('DATABASE_PATH','data/test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET name = "Anonym Användare"')
    conn.commit()
    conn.close()
    print("All user names have been anonymized (GDPR compliant)")
    
def test_fake_users(expected_count=5):
    """Test that fake users are created correctly"""
    db_path = os.getenv('DATABASE_PATH','data/test_users.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # TEST 1: Kontrollera antal
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    assert count == expected_count, f"Datamängden ({count}) avviker från förväntat antal ({expected_count})!"
    print(f"✅ Antalet användare är korrekt: {count}")

    # TEST 2: Kontrollera e-post
    cursor.execute("SELECT COUNT(*) FROM users WHERE email NOT LIKE '%@example%'")
    suspicious = cursor.fetchone()[0]
    assert suspicious == 0, f"Hittade {suspicious} e-postadresser utan '@example'!"
    print("✅ Alla e-postadresser är giltiga (syntetiska)")

    # TEST 3: Kontrollera att inga fält är tomma
    cursor.execute("SELECT COUNT(*) FROM users WHERE name IS NULL OR email IS NULL")
    missing = cursor.fetchone()[0]
    assert missing == 0, f"Hittade {missing} poster med saknad data!"
    print("✅ Inga obligatoriska fält är tomma")

    conn.close()
    print("🎉 Alla GDPR-valideringstest passerade!")

if __name__ == "__main__":
    init_database(num_users=10)
    display_users()

    # Keep the container running for testing
    print("\nContainer is running. Press Ctrl+C to exit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")
