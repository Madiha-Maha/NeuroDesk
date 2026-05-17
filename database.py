import os
import sqlite3

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/neurodesk.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    status TEXT
) 
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
 )
''')

conn.commit()

def add_task(title):
    cursor.execute('INSERT INTO tasks (title, status) VALUES (?, ?)', (title, "pending"))
    conn.commit()

def get_tasks():
    cursor.execute('SELECT * FROM tasks')
    return cursor.fetchall()
    
def update_task_status(task_id):
    cursor.execute('UPDATE tasks SET status = "Completed" WHERE id = ?', (task_id,))
    conn.commit()

def add_note(content):
    cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()

def get_notes():
    cursor.execute('SELECT * FROM notes')
    return cursor.fetchall()