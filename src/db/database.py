import sqlite3
import os


class Database:
    def __init__(self, db_name='database.db'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))

        db_path = os.path.join(project_root, 'db', db_name)

        # Переконуємося, що директорія існує
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_name = db_path
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()


    def create_tables(self) -> None:
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                user_id INTEGER PRIMARY KEY, 
                city TEXT NOT NULL
            )"""
        )

        self.conn.commit()


    def get_city(self, user_id: int) -> str | None:
        self.cursor.execute("SELECT city FROM cities WHERE user_id = ?", (user_id, ))
        results = self.cursor.fetchone()
        return results[0] if results else None


    def add_city(self, user_id: int, name: str) -> None:
        self.cursor.execute("INSERT INTO cities (user_id, city) VALUES (?, ?)", (user_id, name))
        self.conn.commit()


    def edit_city(self, user_id: int, name: str) -> None:
        self.cursor.execute("UPDATE cities SET city = ? WHERE user_id = ?", (name, user_id))
        self.conn.commit()


    def delete_city(self, user_id: int) -> None:
        self.cursor.execute("DELETE FROM cities WHERE user_id = ?", (user_id, ))
        self.conn.commit()


    def close(self) -> None:
        self.conn.close()

