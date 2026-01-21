from flask import Flask, render_template, request, redirect, session, url_for
from config import db
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = "secret123"

# ================== PUBLIC PAGES ==================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/faculty")
def faculty_page():
   
    cursor = db.cursor()
    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()
    cursor.close()
    return render_template("faculty.html", faculty=faculty)

@app.route("/students")
def students_page():
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    return render_template("students.html", students=students)

# ================== ADMIN (HOD) ==================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = db.cursor()
        cursor.execute(
            "SELECT id, username FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        admin = cursor.fetchone()
        cursor.close()

        if admin:
            session["admin"] = admin[1]   # username index
            return redirect("/admin/dashboard")
        else:
            return render_template("admin/login.html", error="Invalid Login")

    return render_template("admin/login.html")


# ================== FACULTY MANAGEMENT ==================
@app.route("/admin/faculty", methods=["GET", "POST"])
def manage_faculty():
    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    # INSERT FACULTY
    if request.method == "POST":
        cursor.execute(
            """
            INSERT INTO faculty
            (name, designation, qualification, experience, subject)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                request.form.get("name"),
                request.form.get("designation"),
                request.form.get("qualification"),
                request.form.get("experience"),
                request.form.get("subject"),
            )
        )
        db.commit()

    # FETCH FACULTY (EXPLICIT COLUMNS)
    cursor.execute(
        """
        SELECT id, name, designation, qualification, experience, subject
        FROM faculty
        ORDER BY name ASC
        """
    )

    faculty = cursor.fetchall()
    cursor.close()

    return render_template("admin/manage_faculty.html", faculty=faculty)

@app.route("/admin/faculty/delete/<int:id>")
def delete_faculty(id):
    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()
    cursor.execute("DELETE FROM faculty WHERE id = %s", (id,))
    db.commit()
    cursor.close()

    return redirect("/admin/faculty")


# ================== STUDENT MANAGEMENT ==================
@app.route("/admin/students", methods=["GET", "POST"])
def manage_students():
    if "admin" not in session:
        return redirect("/admin/login")

    cursor = db.cursor()

    # INSERT STUDENT
    if request.method == "POST":
        cursor.execute(
            """
            INSERT INTO students
            (name, reg_no, "year", section, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                request.form.get("name"),
                request.form.get("reg_no"),
                request.form.get("year"),
                request.form.get("section"),
                request.form.get("email"),
                request.form.get("phone"),
            )
        )
        db.commit()

    # FETCH STUDENTS (EXPLICIT COLUMNS)
    cursor.execute(
        """
        SELECT id, name, reg_no, "year", section, email, phone
        FROM students
        ORDER BY
        CASE "year"
            WHEN '1st BCA' THEN 1
            WHEN '2nd BCA' THEN 2
            WHEN '3rd BCA' THEN 3
        END,
        name ASC
        """
    )

    students = cursor.fetchall()
    cursor.close()

    return render_template("admin/manage_students.html", students=students)

# ================== tem ==================
@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/programs")
def programs_page():
    return render_template("programs.html")



# ================== RUN APP ==================
if __name__ == "__main__":
    app.run()




