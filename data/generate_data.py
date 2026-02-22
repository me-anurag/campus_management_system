import sqlite3
import random

DATABASE = "database.db"

conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

# -------------------------
# Insert Blocks
# -------------------------
blocks = [f"Block {i}" for i in range(32, 40)]

for block in blocks:
    cursor.execute("INSERT INTO blocks (block_name) VALUES (?)", (block,))

# -------------------------
# Insert Classrooms (8 per block)
# -------------------------
cursor.execute("SELECT id FROM blocks")
block_ids = cursor.fetchall()

room_count = 1
for block in block_ids:
    for i in range(1, 9):
        capacity = random.choice([40, 60, 80, 120])
        if random.random() < 0.2:
            current_students = random.randint(int(capacity * 0.95), capacity)  # Overloaded
        elif random.random() < 0.4:
            current_students = random.randint(5, int(capacity * 0.35))  # Underutilized
        else:
            current_students = random.randint(int(capacity * 0.5), int(capacity * 0.85))  # Normal
        room_number = f"R{room_count}"
        cursor.execute("""
            INSERT INTO classrooms (block_id, room_number, capacity, current_students)
            VALUES (?, ?, ?, ?)
        """, (block[0], room_number, capacity, current_students))
        room_count += 1

# -------------------------
# Insert Courses
# -------------------------
courses = [
    "AI", "ML", "DSA", "OS", "CN", "DBMS",
    "Web Dev", "Software Engg", "Cloud", "Cyber Security",
    "Data Mining", "NLP", "IoT", "Robotics",
    "Big Data", "DevOps", "Blockchain",
    "Mobile App Dev", "AR/VR", "Deep Learning"
]

for i, course in enumerate(courses):
    cursor.execute("INSERT INTO courses (course_name, course_code) VALUES (?, ?)",
                   (course, f"CSE{i+101}"))

# -------------------------
# Insert Faculty
# -------------------------
for i in range(1, 26):
    cursor.execute("INSERT INTO faculty (name, department) VALUES (?, ?)",
                   (f"Faculty {i}", "CSE"))

# -------------------------
# Assign Courses to Faculty
# -------------------------
cursor.execute("SELECT id FROM faculty")
faculty_ids = cursor.fetchall()

cursor.execute("SELECT id FROM courses")
course_ids = cursor.fetchall()

for course in course_ids:
    faculty = random.choice(faculty_ids)
    cursor.execute("INSERT INTO course_assignment (faculty_id, course_id) VALUES (?, ?)",
                   (faculty[0], course[0]))

# -------------------------
# Insert Students
# -------------------------
cursor.execute("SELECT id FROM classrooms")
classroom_ids = cursor.fetchall()

for i in range(1, 801):
    course = random.choice(course_ids)
    classroom = random.choice(classroom_ids)

    cursor.execute("""
        INSERT INTO students (name, reg_no, course_id, classroom_id)
        VALUES (?, ?, ?, ?)
    """, (f"Student {i}", f"REG{i:04}", course[0], classroom[0]))

conn.commit()
conn.close()

print("Massive Data Generated Successfully!")