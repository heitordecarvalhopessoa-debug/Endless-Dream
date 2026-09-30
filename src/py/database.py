import sqlite3
import os

class Database:
    def __init__(self):
        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )
        db_path = os.path.join(base_path, "game_stats.db")
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        sql_dir = os.path.join(base_path, "src", "sql")
        self.execute_sql_file(os.path.join(sql_dir, "create_tables.sql"))
        self.execute_sql_file(os.path.join(sql_dir, "init_data.sql"))
        
        self.ensure_table_exists()

    def execute_sql_file(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    script = f.read()
                    self.cursor.executescript(script)
                self.conn.commit()
            except Exception as e:
                print(f"SQL execution warning: {e}")

    def ensure_table_exists(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS player_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_pages_collected INTEGER DEFAULT 0,
                    max_level_reached INTEGER DEFAULT 0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.cursor.execute('SELECT COUNT(*) FROM player_progress')
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO player_progress (id, total_pages_collected, max_level_reached) VALUES (1, 0, 0)')
            self.conn.commit()
        except Exception as e:
            print(f"Error ensuring table exists: {e}")

    def get_stats(self):
        try:
            self.cursor.execute('SELECT total_pages_collected, max_level_reached FROM player_progress WHERE id = 1')
            row = self.cursor.fetchone()
            return row if row else (0, 0)
        except Exception:
            return (0, 0)

    def update_stats(self, pages_to_add, current_level):
        try:
            pages, high_lvl = self.get_stats()
            new_total_pages = pages + pages_to_add
            new_highest_level = max(high_lvl, current_level)
            self.cursor.execute('''
                UPDATE player_progress SET total_pages_collected = ?, max_level_reached = ?, last_updated = CURRENT_TIMESTAMP WHERE id = 1
            ''', (new_total_pages, new_highest_level))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating stats: {e}")