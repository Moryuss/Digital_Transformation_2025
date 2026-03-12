import sqlite3

def add_doc_to_sqlite_db(id, page, doc_content):
    conn = sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO docs VALUES (?, ?, ?)",(id, page, doc_content))
    conn.commit()
    conn.close()

def createDB():
    conn =sqlite3.connect("rag.db")
    cursor = conn.cursor()
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS docs (
                id INTEGER PRIMARY KEY,
                page INTEGER,
                doc_content TEXT
                )
                """)
    conn.close()