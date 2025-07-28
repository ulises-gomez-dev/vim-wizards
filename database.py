#!/usr/bin/env python3
"""
Database module for VimWizards high score management.
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


class ScoreDatabase:

    def __init__(self, db_path: str = "./data/scores.db"):
        # Initialize database connection.
        self._db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        # Create the database and high_scores table if they don't exist.
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS high_scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        initials TEXT NOT NULL CHECK(length(initials) = 3),
                        score INTEGER NOT NULL CHECK(score >= 0),
                        date TEXT NOT NULL
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
    
    def save_score(self, initials: str, score: int, date: Optional[str] = None) -> bool:
        """
        Save a new high score entry.
        
        Args:
            initials: Player's 3-character initials (will be converted to uppercase)
            score: Player's score (must be non-negative)
            date: Optional date string (defaults to current date/time)
        
        Returns:
            True if save was successful, False otherwise
        """
        if len(initials) != 3:
            print("Error: Initials must be exactly 3 characters")
            return False
        
        if score < 0:
            print("Error: Score cannot be negative")
            return False
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    "INSERT INTO high_scores (initials, score, date) VALUES (?, ?, ?)",
                    (initials.upper(), score, date)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error saving score: {e}")
            return False
    
    def get_top_scores(self, limit: int = 10) -> List[Tuple[str, int, str]]:
        """
        Get the top high scores ordered by score descending.
        
        Args:
            limit: Maximum number of scores to return (default 10)
        
        Returns:
            List of tuples containing (initials, score, date)
        """
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute(
                    "SELECT initials, score, date FROM high_scores ORDER BY score DESC LIMIT ?",
                    (limit,)
                )
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving scores: {e}")
            return []
    
    def get_score_count(self) -> int:
        """Get the total number of scores in the database."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM high_scores")
                return cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(f"Error counting scores: {e}")
            return 0
    
    def clear_scores(self) -> bool:
        """Clear all scores from the database. Use with caution."""
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute("DELETE FROM high_scores")
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error clearing scores: {e}")
            return False


def init_database(db_path: str = "scores.db") -> None:
    """
    Initialize the high scores database.
    
    Args:
        db_path: Path to the database file (default: scores.db)
    """
    db = ScoreDatabase(db_path)


def save_high_score(initials: str, score: int, date: Optional[str] = None, db_path: str = "scores.db") -> bool:
    """
    Save a new high score entry.
    
    Args:
        initials: Player's 3-character initials
        score: Player's score
        date: Optional date string (defaults to current date/time)
        db_path: Path to the database file
    
    Returns:
        True if save was successful, False otherwise
    """
    db = ScoreDatabase(db_path)
    return db.save_score(initials, score, date)


def get_top_high_scores(limit: int = 10, db_path: str = "scores.db") -> List[Tuple[str, int, str]]:
    """
    Get the top high scores ordered by score descending.
    
    Args:
        limit: Maximum number of scores to return (default 10)
        db_path: Path to the database file
    
    Returns:
        List of tuples containing (initials, score, date)
    """
    db = ScoreDatabase(db_path)
    return db.get_top_scores(limit)


def test_database():
    """Test the database functionality."""
    # Use a test database file
    test_db = "test_scores.db"
    
    print("Testing database functionality...")
    
    # Initialize database
    init_database(test_db)
    print("Database initialized")
    
    # Save some test scores
    test_scores = [
        ("AAA", 100),
        ("BBB", 250),
        ("CCC", 175),
        ("DDD", 300),
        ("EEE", 50)
    ]
    
    for initials, score in test_scores:
        if save_high_score(initials, score, db_path=test_db):
            print(f"Saved score: {initials} - {score}")
        else:
            print(f"Failed to save score: {initials} - {score}")
    
    # Retrieve and display top scores
    print("\nTop 5 High Scores:")
    top_scores = get_top_high_scores(5, test_db)
    for i, (initials, score, date) in enumerate(top_scores, 1):
        print(f"{i}. {initials} - {score} ({date})")
    
    # Clean up test database
    if os.path.exists(test_db):
        os.remove(test_db)
        print(f"\nTest database {test_db} removed")


if __name__ == "__main__":
    test_database()
