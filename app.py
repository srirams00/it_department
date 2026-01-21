from flask import Flask, render_template, request, redirect, session, url_for
from config import db

app = Flask(__name__)
app.secret_key = "secret123"

# ================== PUBLIC PAGES ==================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/faculty")
def faculty_page():
   
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()
    return render_template("faculty.html", faculty=faculty)

@app.route("/students")
def students_page():
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("students.html", students=students)

# ================== ADMIN (HOD) ==================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cursor.fetchone()

        if admin:
            session["admin"] = admin["username"]
            return redirect("/admin/dashboard")
        else:
            return render_template("admin/login.html", error="Invalid Login")

    return render_template("admin/login.html")

@app.route("/admin/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect("/admin/login")
    return render_template("admin/dashboard.html")

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect("/")

# ================== FACULTY MANAGEMENT ==================
@app.route("/admin/faculty", methods=["GET", "POST"])
def manage_faculty():
    if "admin" not in session:
        return redirect("/admin/login")

   
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute(
            "INSERT INTO faculty (name, designation, qualification, experience, subject) VALUES (%s,%s,%s,%s,%s)",
            (request.form["name"], request.form["designation"],
             request.form["qualification"], request.form["experience"],
             request.form["subject"])
        )
        db.commit()

    cursor.execute("SELECT * FROM faculty")
    faculty = cursor.fetchall()
    return render_template("admin/manage_faculty.html", faculty=faculty)

@app.route("/admin/faculty/delete/<int:id>")
def delete_faculty(id):
    
    cursor = db.cursor()
    cursor.execute("DELETE FROM faculty WHERE id=%s", (id,))
    db.commit()
    return redirect("/admin/faculty")

# ================== STUDENT MANAGEMENT ==================
@app.route("/admin/students", methods=["GET", "POST"])
def manage_students():
    if "admin" not in session:
        return redirect("/admin/login")

   
    cursor = db.cursor(dictionary=True)

    if request.method == "POST":
        cursor.execute(
            "INSERT INTO students (name, reg_no, year, section, email, phone) VALUES (%s,%s,%s,%s,%s,%s)",
            (request.form["name"], request.form["reg_no"],
             request.form["year"], request.form["section"],
             request.form["email"], request.form["phone"])
        )
        db.commit()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template("admin/manage_students.html", students=students)

@app.route("/admin/students/delete/<int:id>")
def delete_student(id):
   
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()
    return redirect("/admin/students")

@app.route("/about")
def about_page():
    return render_template("about.html")

@app.route("/programs")
def programs_page():
    return render_template("programs.html")



# ================== RUN APP ==================
if __name__ == "__main__":
    app.run(debug=True)




