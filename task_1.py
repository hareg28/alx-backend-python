#!/usr/bin/env python3
"""
Task 1: Reusable query context manager
"""

import sqlite3


class ExecuteQuery:
    """Context manager for executing queries with parameters"""

    def __init__(self, query, params=()):
        """Initialize with query and optional parameters"""
        self.query = query
        self.params = params

    def __enter__(self):
        """Open database connection and execute query"""
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection"""
        self.conn.close()


if __name__ == "__main__":
    # Example usage
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        for user in results:
            print(user)
