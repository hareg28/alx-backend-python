#!/usr/bin/env python3
"""
Task 0: Custom class-based context manager for database connection
"""

import sqlite3


class DatabaseConnection:
    """Context manager for handling SQLite database connections"""

    def __init__(self, db_name):
        """Initialize with database name"""
        self.db_name = db_name

    def __enter__(self):
        """Open database connection"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection"""
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
