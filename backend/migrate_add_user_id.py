"""
Migration script to add user_id column to patient_data table
Run this once to update the existing database schema
"""
import sqlite3

def migrate_database():
    conn = sqlite3.connect("diabetes_prediction.db")
    cursor = conn.cursor()
    
    try:
        # Check if user_id column already exists
        cursor.execute("PRAGMA table_info(patient_data)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'user_id' not in columns:
            print("Adding user_id column to patient_data table...")
            cursor.execute("""
                ALTER TABLE patient_data 
                ADD COLUMN user_id INTEGER
            """)
            
            # Create an index on user_id for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_patient_data_user_id 
                ON patient_data(user_id)
            """)
            
            conn.commit()
            print("✅ Migration completed successfully!")
            print("Note: Existing records will have user_id = NULL")
        else:
            print("✅ user_id column already exists. No migration needed.")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
