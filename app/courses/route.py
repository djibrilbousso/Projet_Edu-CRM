from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import add_course, list_courses, delete_course

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')

@courses_bp.route('/')
def index():
    courses = list_courses()
    return render_template('courses/list.html', courses=courses)


@courses_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        teacher_id = request.form.get('teacher_id')
        
        if not title or not teacher_id:
            flash('Tous les champs sont obligatoires', 'danger')
            return redirect(url_for('courses.create'))
        
        add_course(title, int(teacher_id))
        flash('Cours ajouté avec succès', 'success')
        return redirect(url_for('courses.index'))
    
    return render_template('courses/create.html')


@courses_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_course(id)
    flash('Cours supprimé', 'success')
    return redirect(url_for('courses.index'))