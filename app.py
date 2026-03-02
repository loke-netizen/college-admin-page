from flask import Flask,render_template,request,redirect  
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

    # DATABASE CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///college.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Department(db.Model):
    dept_id = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(100), nullable=False)

class Staff(db.Model):
        staff_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

class Student(db.Model):
        student_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))

class Subject(db.Model):
        subject_id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        dept_id = db.Column(db.Integer, db.ForeignKey('department.dept_id'))
        staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'))

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
            return redirect("/homepage")
        else:
            return render_template("login.html", error="Invalid Username or Password")
@app.route("/homepage")
def domain():
    page = request.args.get("page")

    if page == "department":
        departments = Department.query.all()
        return render_template("index.html",
                               page="department",
                               departments=departments)

    elif page == "student":
        students = Student.query.all()
        return render_template("index.html",
                               page="student",
                               students=students)

    elif page == "staff":
        staffs = Staff.query.all()
        return render_template("index.html",
                               page="staff",
                               staffs=staffs)

    elif page == "subject":
        subjects = Subject.query.all()
        return render_template("index.html",
                               page="subject",
                               subjects=subjects)

    return render_template("index.html", page="dashboard")
@app.route("/departments")
def departments():
        all_depts = Department.query.all()
        return render_template("departments.html", departments=all_depts)        
with app.app_context():
        db.create_all()
with app.app_context():
    if not Department.query.first():
        sample = Department(dept_name="Computer Science")
        db.session.add(sample)
        db.session.commit()

if __name__=="__main__":
        app.run(debug=True)