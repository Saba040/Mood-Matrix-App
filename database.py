import sqlite3

class Database:
    def __init__(self, db_name='data.sqlite3'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        mood TEXT NOT NULL,
        date TEXT,
        productivity INTEGER
    )
        """)
        self.conn.commit()
        print("[DB] Table ready.")





    def add_task(self, task, mood, date, productivity):
        self.cursor.execute("""
        INSERT INTO tasks (task, mood, date, productivity)
        VALUES (?, ?, ?, ?)
        """, (task, mood, date, productivity))

        self.conn.commit()

    def show_tasks(self):
        return self.cursor.execute("SELECT * FROM tasks").fetchall()

    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()

    def edit_task(self, task_id, task, mood, date, productivity):
        self.cursor.execute("""
        UPDATE tasks
        SET task=?, mood=?, date=?, productivity=?
        WHERE id=?
        """, (task, mood, date, productivity, task_id))

        self.conn.commit()

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, date, task, mood, productivity FROM tasks")
        return cursor.fetchall()
