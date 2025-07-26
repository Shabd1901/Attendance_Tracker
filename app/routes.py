from flask import Blueprint, render_template, redirect, url_for, request, session
from .models import Student, Attendance
from . import db
from datetime import date

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    students = Student.query.all()
    session['current'] = 0  # Reset progress
    return render_template('home.html', students=students)

@bp.route('/start')
def start_attendance():
    session['current'] = 0
    return redirect(url_for('main.attendance'))

@bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    students = Student.query.all()
    total = len(students)
    idx = session.get('current', 0)

    if idx >= total:
        return render_template('attendance.html', complete=True)

    current_student = students[idx]

    if request.method == 'POST':
        status = request.form['status']
        new_record = Attendance(
            student_id=current_student.id,
            status=status
        )
        db.session.add(new_record)
        db.session.commit()
        session['current'] += 1
        return redirect(url_for('main.attendance'))

    return render_template('attendance.html', student=current_student, complete=False)

@bp.route('/summary')
def summary():
    today = date.today()
    records = Attendance.query.filter_by(date=today).all()
    return render_template('view_class.html', records=records)
