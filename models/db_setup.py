import sqlite3

def create_connection():
    conn = sqlite3.connect("database.db")
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # USERS TABLE (Login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    # BLOCKS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_name TEXT NOT NULL
    )
    """)

    # CLASSROOMS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classrooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_id INTEGER,
        room_number TEXT,
        capacity INTEGER,
        current_students INTEGER,
        FOREIGN KEY(block_id) REFERENCES blocks(id)
    )
    """)

    # COURSES
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        course_code TEXT
    )
    """)

    # FACULTY
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT
    )
    """)

    # COURSE ASSIGNMENT (Faculty workload)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS course_assignment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        faculty_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY(faculty_id) REFERENCES faculty(id),
        FOREIGN KEY(course_id) REFERENCES courses(id)
    )
    """)

    # STUDENTS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        reg_no TEXT,
        course_id INTEGER,
        classroom_id INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(id),
        FOREIGN KEY(classroom_id) REFERENCES classrooms(id)
    )
    """)

    conn.commit()
    conn.close()

def create_admin():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES ('admin', 'admin123', 'admin')
        """)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    create_tables()
    create_admin()
    print("Database & Tables Created Successfully!")