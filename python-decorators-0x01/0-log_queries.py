#!/usr/bin/env python3
import sqlite3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing the function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query", "") if "query" in kwargs else args[0]
        print(f"Executing query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
users = fetch_all_users(query="SELECT * FROM users")
