import sqlite3
import os
import logging

logger = logging.getLogger("kitchen_os")

class DatabaseManager:
    def __init__(self, db_path="database/kitchen_os.db"):
        self.db_path = db_path
        # Ensure database directory exists
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # Enable foreign keys
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        schema_path = "database/schema.sql"
        if not os.path.exists(schema_path):
            schema_path = "../database/schema.sql" # fallback for dev path execution
        
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            conn = self.get_connection()
            try:
                conn.executescript(schema_sql)
                conn.commit()
                logger.info("Database schema initialized successfully.")
            except Exception as e:
                logger.error(f"Error initializing schema: {e}")
            finally:
                conn.close()
        else:
            logger.warning("schema.sql file not found. Skipping initialization.")

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Fetch all failed: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Fetch one failed: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    # --- INTENTIONAL DEFECT #8: Database Connection Leak on Exception ---
    # The find_user_by_email method does not close the cursor or connection when an exception occurs.
    # This leads to connection/file descriptor leaks over time when invalid queries are executed.
    def find_user_by_email(self, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            # DEFECT: missing cursor.close() and conn.close() in this block
            raise e
