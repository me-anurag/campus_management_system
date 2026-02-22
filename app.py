from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"
DATABASE = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = user["username"]
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")
# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    total_blocks = conn.execute("SELECT COUNT(*) FROM blocks").fetchone()[0]
    total_classrooms = conn.execute("SELECT COUNT(*) FROM classrooms").fetchone()[0]
    total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    total_faculty = conn.execute("SELECT COUNT(*) FROM faculty").fetchone()[0]

    # CAMPUS UTILIZATION
    campus = conn.execute("""
        SELECT SUM(current_students) as total_students,
               SUM(capacity) as total_capacity
        FROM classrooms
    """).fetchone()

    campus_util = 0
    if campus["total_capacity"]:
        campus_util = round((campus["total_students"] / campus["total_capacity"]) * 100, 2)

    # CLASSROOM DATA
    classrooms = conn.execute("SELECT * FROM classrooms").fetchall()

    overloaded = []
    underutilized = []

    room_labels = []
    room_utilization = []
    room_colors = []

    for room in classrooms:
        util = 0
        if room["capacity"]:
            util = round((room["current_students"] / room["capacity"]) * 100, 2)

        room_labels.append(room["room_number"])
        room_utilization.append(util)

        if util > 90:
            overloaded.append(room["room_number"])
            room_colors.append("rgba(255,99,132,0.7)")
        elif util < 40:
            underutilized.append(room["room_number"])
            room_colors.append("rgba(54,162,235,0.7)")
        else:
            room_colors.append("rgba(75,192,192,0.7)")

    # SMART RECOMMENDATION
    recommendations = []
    if overloaded and underutilized:
        recommendations.append(
            f"Move students from {overloaded[0]} to {underutilized[0]}"
        )

    # BLOCK UTILIZATION
    block_data = conn.execute("""
        SELECT blocks.block_name,
               SUM(classrooms.current_students) as total_students,
               SUM(classrooms.capacity) as total_capacity
        FROM blocks
        JOIN classrooms ON blocks.id = classrooms.block_id
        GROUP BY blocks.id
    """).fetchall()

    block_labels = []
    block_util = []

    for b in block_data:
        if b["total_capacity"]:
            util = round((b["total_students"] / b["total_capacity"]) * 100, 2)
        else:
            util = 0

        block_labels.append(b["block_name"])
        block_util.append(util)

    conn.close()

    return render_template(
        "dashboard.html",
        total_blocks=total_blocks,
        total_classrooms=total_classrooms,
        total_students=total_students,
        total_faculty=total_faculty,
        campus_util=campus_util,
        overloaded=overloaded,
        underutilized=underutilized,
        recommendations=recommendations,
        room_labels=room_labels,
        room_utilization=room_utilization,
        room_colors=room_colors,
        block_labels=block_labels,
        block_util=block_util
    )
# ---------------- BLOCK CRUD ----------------
@app.route("/blocks")
def blocks():
    conn = get_db_connection()
    blocks = conn.execute("SELECT * FROM blocks").fetchall()
    conn.close()
    return render_template("blocks.html", blocks=blocks)

@app.route("/add_block", methods=["POST"])
def add_block():
    name = request.form["block_name"]
    conn = get_db_connection()
    conn.execute("INSERT INTO blocks (block_name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect("/blocks")

@app.route("/delete_block/<int:id>")
def delete_block(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM blocks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/blocks")

# ---------------- CLASSROOM CRUD ----------------
@app.route("/classrooms")
def classrooms():
    block_filter = request.args.get("block")
    conn = get_db_connection()

    if block_filter:
        rooms = conn.execute("SELECT * FROM classrooms WHERE block_id=?",
                             (block_filter,)).fetchall()
    else:
        rooms = conn.execute("SELECT * FROM classrooms").fetchall()

    blocks = conn.execute("SELECT * FROM blocks").fetchall()
    conn.close()
    return render_template("classrooms.html", rooms=rooms, blocks=blocks)

@app.route("/add_classroom", methods=["POST"])
def add_classroom():
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO classrooms (block_id, room_number, capacity, current_students)
        VALUES (?, ?, ?, ?)
    """, (request.form["block_id"],
          request.form["room_number"],
          request.form["capacity"],
          request.form["current_students"]))
    conn.commit()
    conn.close()
    return redirect("/classrooms")

@app.route("/delete_classroom/<int:id>")
def delete_classroom(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM classrooms WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/classrooms")

# ---------------- COURSE CRUD ----------------
@app.route("/courses")
def courses():
    conn = get_db_connection()
    courses = conn.execute("SELECT * FROM courses").fetchall()
    conn.close()
    return render_template("courses.html", courses=courses)

@app.route("/add_course", methods=["POST"])
def add_course():
    conn = get_db_connection()
    conn.execute("INSERT INTO courses (course_name, course_code) VALUES (?, ?)",
                 (request.form["course_name"], request.form["course_code"]))
    conn.commit()
    conn.close()
    return redirect("/courses")

@app.route("/delete_course/<int:id>")
def delete_course(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM courses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/courses")

# ---------------- FACULTY CRUD ----------------
@app.route("/faculty")
def faculty():
    conn = get_db_connection()
    faculty = conn.execute("SELECT * FROM faculty").fetchall()
    conn.close()
    return render_template("faculty.html", faculty=faculty)

@app.route("/add_faculty", methods=["POST"])
def add_faculty():
    conn = get_db_connection()
    conn.execute("INSERT INTO faculty (name, department) VALUES (?, ?)",
                 (request.form["name"], request.form["department"]))
    conn.commit()
    conn.close()
    return redirect("/faculty")

@app.route("/delete_faculty/<int:id>")
def delete_faculty(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM faculty WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/faculty")

# ---------------- STUDENT CRUD ----------------
@app.route("/students")
def students():
    course_filter = request.args.get("course")
    conn = get_db_connection()

    if course_filter:
        students = conn.execute("SELECT * FROM students WHERE course_id=?",
                                (course_filter,)).fetchall()
    else:
        students = conn.execute("SELECT * FROM students").fetchall()

    courses = conn.execute("SELECT * FROM courses").fetchall()
    classrooms = conn.execute("SELECT * FROM classrooms").fetchall()
    conn.close()

    return render_template("students.html",
                           students=students,
                           courses=courses,
                           classrooms=classrooms)

@app.route("/add_student", methods=["POST"])
def add_student():
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO students (name, reg_no, course_id, classroom_id)
        VALUES (?, ?, ?, ?)
    """, (request.form["name"],
          request.form["reg_no"],
          request.form["course_id"],
          request.form["classroom_id"]))
    conn.commit()
    conn.close()
    return redirect("/students")

@app.route("/delete_student/<int:id>")
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/students")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)