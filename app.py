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

    # Classroom Utilization
    classrooms = conn.execute("SELECT room_number, capacity, current_students FROM classrooms").fetchall()

    room_labels = []
    utilization_data = []
    bar_colors = []

    overloaded_rooms = []
    underutilized_rooms = []

    for room in classrooms:
        if room["capacity"] > 0:
            utilization = (room["current_students"] / room["capacity"]) * 100
        else:
            utilization = 0

        utilization = round(utilization, 2)

        room_labels.append(room["room_number"])
        utilization_data.append(utilization)

        if utilization > 90:
            overloaded_rooms.append({
                "room": room["room_number"],
                "util": utilization
            })
            bar_colors.append("rgba(255, 99, 132, 0.7)")
        elif utilization < 40:
            underutilized_rooms.append({
                "room": room["room_number"],
                "util": utilization
            })
            bar_colors.append("rgba(54, 162, 235, 0.7)")
        else:
            bar_colors.append("rgba(75, 192, 192, 0.7)")

    # Block Utilization
    block_data = conn.execute("""
        SELECT blocks.block_name,
               SUM(classrooms.current_students) as total_students,
               SUM(classrooms.capacity) as total_capacity
        FROM blocks
        JOIN classrooms ON blocks.id = classrooms.block_id
        GROUP BY blocks.id
    """).fetchall()

    block_labels = []
    block_utilization = []

    for block in block_data:
        if block["total_capacity"] > 0:
            util = (block["total_students"] / block["total_capacity"]) * 100
        else:
            util = 0

        block_labels.append(block["block_name"])
        block_utilization.append(round(util, 2))

    # Student Distribution
    course_data = conn.execute("""
        SELECT courses.course_name, COUNT(students.id) as total
        FROM courses
        LEFT JOIN students ON courses.id = students.course_id
        GROUP BY courses.id
    """).fetchall()

    course_labels = []
    course_counts = []

    for c in course_data:
        course_labels.append(c["course_name"])
        course_counts.append(c["total"])

    # Faculty Workload
    faculty_data = conn.execute("""
        SELECT faculty.name, COUNT(course_assignment.course_id) as workload
        FROM faculty
        LEFT JOIN course_assignment ON faculty.id = course_assignment.faculty_id
        GROUP BY faculty.id
    """).fetchall()

    faculty_labels = []
    faculty_workload = []

    for f in faculty_data:
        faculty_labels.append(f["name"])
        faculty_workload.append(f["workload"])

    conn.close()

    return render_template(
        "dashboard.html",
        total_blocks=total_blocks,
        total_classrooms=total_classrooms,
        total_students=total_students,
        total_faculty=total_faculty,
        room_labels=room_labels,
        utilization_data=utilization_data,
        bar_colors=bar_colors,
        overloaded_rooms=overloaded_rooms,
        underutilized_rooms=underutilized_rooms,
        block_labels=block_labels,
        block_utilization=block_utilization,
        course_labels=course_labels,
        course_counts=course_counts,
        faculty_labels=faculty_labels,
        faculty_workload=faculty_workload
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)