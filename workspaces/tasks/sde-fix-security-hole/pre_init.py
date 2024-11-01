import os
import logging
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO,    
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()  # Log messages to the console
    ])
logger = logging.getLogger("Pre-Init Test")

def test_database_exists():
    """Test if the events database exists."""
    db_path = os.path.join('/workspace/TheAgentCompany/workspaces/tasks/sde-fix-security-hole/events-viewer/events.db')
    if not os.path.exists(db_path):
        logger.error("Events database does not exist")
        return False
    
    # Try to connect to the database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        if not cursor.fetchone():
            logger.error("Events table does not exist in database")
            return False
        conn.close()
        return True
    except sqlite3.Error as e:
        logger.error(f"Error accessing database: {e}")
        return False

if __name__ == "__main__":
    if not test_database_exists():
        raise Exception("Failed to verify database setup")
    