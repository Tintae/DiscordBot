import sqlite3


class InvalidUserIdError(Exception):
    """Raised when the provided user ID is not valid."""
    pass


class SongPlaysDatabase:
    def __init__(self):
        self.DATABASE_FILE = 'data/song_plays.db'  # Make sure the path is correct relative to bot.py
        self.create_database()

    def create_database(self):
        """Creates the database and table if they don't exist."""
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS song_plays (
                        user_id INTEGER NOT NULL PRIMARY KEY,
                        plays INTEGER NOT NULL DEFAULT 0
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def increment_plays(self, user_id):
        """Increments the play count for a user."""
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO song_plays (user_id, plays)
                    VALUES (?, COALESCE((SELECT plays FROM song_plays WHERE user_id = ?), 0) + 1)
                    ON CONFLICT(user_id) DO UPDATE SET plays = plays + 1
                ''', (user_id, user_id))
                conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def get_plays(self, user_id):
        """Retrieves the play count for a user."""
        if not isinstance(user_id, int) or user_id <= 0:
            raise InvalidUserIdError("User ID must be a positive integer.")

        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT plays FROM song_plays WHERE user_id = ?
                ''', (user_id,))
                result = cursor.fetchone()
                return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def list_all_plays(self):
        """Returns a list of tuples containing (user_id, plays) for all users."""
        try:
            with sqlite3.connect(self.DATABASE_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id, plays FROM song_plays
                ''')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
