from flask import Blueprint, render_template
from app.utils import login_required
from app.services.student_service import list_students
from app.services.teacher_service import list_teachers
from app.services.course_service import list_courses

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    nb_students = len(list_students())
    nb_teachers = len(list_teachers())
    nb_courses = len(list_courses())
    return render_template('dashboard/index.html',
                           nb_students=nb_students,
                           nb_teachers=nb_teachers,
                           nb_courses=nb_courses)
