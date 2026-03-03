from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False)

    students = db.relationship("Student", backref="department", lazy=True)
    staffs = db.relationship("Staff", backref="department", lazy=True)
    subjects = db.relationship("Subject", backref="department", lazy=True)


class Staff(db.Model):
    staff_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

    subjects = db.relationship("Subject", backref="staff", lazy=True)


class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))


class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))
# ================= LOGIN =================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/homepage", methods=["POST"])
def home():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return redirect("/homepage?page=dashboard")
    else:
        return render_template("login.html", error="Invalid Username or Password")

# ================= MAIN PAGE =================

@app.route("/homepage")
def domain():
    page = request.args.get("page")

    if not page:
        page = "dashboard"

    departments = Department.query.all()
    students = Student.query.all()
    staffs = Staff.query.all()
    subjects = Subject.query.all()

    return render_template("index.html",
                           page=page,
                           departments=departments,
                           students=students,
                           staffs=staffs,
                           subjects=subjects)

# ================= DEPARTMENT CRUD =================

@app.route("/department/add", methods=["POST"])
def add_department():
    name = request.form["dept_name"]
    new_dept = Department(dept_name=name)
    db.session.add(new_dept)
    db.session.commit()
    return redirect("/homepage?page=department")

@app.route("/department/edit/<int:id>", methods=["POST"])
def edit_department(id):
    dept = Department.query.get(id)
    dept.dept_name = request.form["dept_name"]
    db.session.commit()
    return redirect("/homepage?page=department")

@app.route("/department/delete/<int:id>")
def delete_department(id):
    dept = Department.query.get(id)
    db.session.delete(dept)
    db.session.commit()
    return redirect("/homepage?page=department")

# ================= STUDENT CRUD =================

@app.route("/student/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    dept_id = request.form["dept_id"]
    new_student = Student(name=name, dept_id=dept_id)
    db.session.add(new_student)
    db.session.commit()
    return redirect("/homepage?page=student")

@app.route("/student/edit/<int:id>", methods=["POST"])
def edit_student(id):
    student = Student.query.get(id)
    student.name = request.form["name"]
    student.dept_id = request.form["dept_id"]
    db.session.commit()
    return redirect("/homepage?page=student")

@app.route("/student/delete/<int:id>")
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect("/homepage?page=student")

# ================= STAFF CRUD =================

@app.route("/staff/add", methods=["POST"])
def add_staff():
    name = request.form["name"]
    dept_id = request.form["dept_id"]
    new_staff = Staff(name=name, dept_id=dept_id)
    db.session.add(new_staff)
    db.session.commit()
    return redirect("/homepage?page=staff")

@app.route("/staff/edit/<int:id>", methods=["POST"])
def edit_staff(id):
    staff = Staff.query.get(id)
    staff.name = request.form["name"]
    staff.dept_id = request.form["dept_id"]
    db.session.commit()
    return redirect("/homepage?page=staff")

@app.route("/staff/delete/<int:id>")
def delete_staff(id):
    staff = Staff.query.get(id)
    db.session.delete(staff)
    db.session.commit()
    return redirect("/homepage?page=staff")

# ================= SUBJECT CRUD =================

@app.route("/subject/add", methods=["POST"])
def add_subject():
    name = request.form["name"]
    dept_id = request.form["dept_id"]
    staff_id = request.form["staff_id"]

    new_subject = Subject(name=name,
                          dept_id=dept_id,
                          staff_id=staff_id)

    db.session.add(new_subject)
    db.session.commit()
    return redirect("/homepage?page=subject")

@app.route("/subject/edit/<int:id>", methods=["POST"])
def edit_subject(id):
    subject = Subject.query.get(id)
    subject.name = request.form["name"]
    subject.dept_id = request.form["dept_id"]
    subject.staff_id = request.form["staff_id"]
    db.session.commit()
    return redirect("/homepage?page=subject")

@app.route("/subject/delete/<int:id>")
def delete_subject(id):
    subject = Subject.query.get(id)
    db.session.delete(subject)
    db.session.commit()
    return redirect("/homepage?page=subject")

# ================= DB INIT =================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
