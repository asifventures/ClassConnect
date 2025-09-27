from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ✅ MySQL connection (password encoded because of @)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Asif%402006@localhost/classconnect"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODELS ---------------- #
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Present / Absent

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return "Welcome to ClassConnect 🚀"

# ---------- User Routes ---------- #
@app.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    user = User(username=data["username"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users])

# ---------- Timetable Routes ---------- #
@app.route("/timetable", methods=["POST"])
def add_timetable():
    data = request.get_json()
    timetable = Timetable(
        subject=data["subject"], teacher=data["teacher"],
        day=data["day"], time=data["time"]
    )
    db.session.add(timetable)
    db.session.commit()
    return jsonify({"message": "Timetable added!"})

@app.route("/timetable", methods=["GET"])
def get_timetable():
    timetables = Timetable.query.all()
    return jsonify([
        {"id": t.id, "subject": t.subject, "teacher": t.teacher, "day": t.day, "time": t.time}
        for t in timetables
    ])

# ---------- Attendance Routes ---------- #
@app.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    attendance = Attendance(
        student_name=data["student_name"], date=data["date"], status=data["status"]
    )
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Attendance marked!"})

@app.route("/attendance", methods=["GET"])
def get_attendance():
    records = Attendance.query.all()
    return jsonify([
        {"id": a.id, "student_name": a.student_name, "date": a.date, "status": a.status}
        for a in records
    ])

# ---------------- MAIN ---------------- #
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
