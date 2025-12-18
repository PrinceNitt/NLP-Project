"""
Database Connection Examples
Database se connect karne ke tarike
"""

from utils.database import get_db_connection, init_database
import sqlite3

# Step 1: Pehle database initialize karein
print("Initializing database...")
init_database()
print("Database initialized successfully!")

# Method 1: Context Manager use karke (Recommended)
# Ye automatic cleanup karta hai
print("\n--- Method 1: Context Manager ---")
try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Example query
        cursor.execute("SELECT COUNT(*) as count FROM user_uploaded_pdfs")
        result = cursor.fetchone()
        print(f"Total PDFs in database: {result['count']}")
        
        # Aap yahan koi bhi query run kar sakte hain
        # Connection automatically close ho jayega
        
except sqlite3.Error as e:
    print(f"Database error: {e}")

# Method 2: Custom Query Example
print("\n--- Method 2: Custom Query Example ---")
def get_custom_data():
    """Custom query run karne ka example"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Aapki custom query
            cursor.execute("""
                SELECT id, name, uploaded_at 
                FROM user_uploaded_pdfs 
                ORDER BY uploaded_at DESC 
                LIMIT 5
            """)
            
            results = cursor.fetchall()
            for row in results:
                print(f"ID: {row['id']}, Name: {row['name']}, Date: {row['uploaded_at']}")
                
            return results
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []

# Method 3: Data Insert Example
print("\n--- Method 3: Data Insert Example ---")
def insert_custom_data(name: str, data: bytes):
    """Data insert karne ka example"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO user_uploaded_pdfs (name, data, file_size) VALUES (?, ?, ?)',
                (name, data, len(data))
            )
            record_id = cursor.lastrowid
            print(f"Data inserted successfully! ID: {record_id}")
            return record_id
    except sqlite3.Error as e:
        print(f"Insert error: {e}")
        return None

# Method 4: Multiple Operations
print("\n--- Method 4: Multiple Operations ---")
def multiple_operations():
    """Ek hi connection mein multiple operations"""
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Operation 1: Count
            cursor.execute("SELECT COUNT(*) as count FROM user_uploaded_pdfs")
            count = cursor.fetchone()['count']
            print(f"Total records: {count}")
            
            # Operation 2: Get all names
            cursor.execute("SELECT name FROM user_uploaded_pdfs")
            names = [row['name'] for row in cursor.fetchall()]
            print(f"All file names: {names}")
            
            # Sab operations automatically commit ho jayenge
            # Connection automatically close ho jayega
    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("Database Connection Examples")
    print("=" * 50)
    
    # Examples run karein
    get_custom_data()
    multiple_operations()
    
    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)

