from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import add_course, list_courses, delete_course
from app.services.teacher_service import list_teachers
from app.utils import login_required, paginate

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")

@courses_bp.route("/")
@login_required
def index():
    all_courses = list_courses()
    page = request.args.get("page", 1, type=int)
    courses_page, total_pages = paginate(all_courses, page)
    url_pagination = url_for('courses.index')
    return render_template("courses/list.html", courses=courses_page,
                           page=page, total_pages=total_pages, url_pagination=url_pagination)

@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    teachers = list_teachers()
    if request.method == "POST":
        title = request.form.get("title")
        teacher_id = request.form.get("teacher_id")
        
        if not title or not teacher_id:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("courses.create"))
        
        result = add_course(title, int(teacher_id))
        if result is None:
            flash("Ce cours existe déjà", "danger")
            return redirect(url_for("courses.create"))
        if result is False:
            flash("Enseignant non trouvé", "danger")
            return redirect(url_for("courses.create"))
        
        flash("Cours ajouté avec succès", "success")
        return redirect(url_for("courses.index"))
    
    return render_template("courses/create.html", teachers=teachers)

@courses_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    delete_course(id)
    flash("Cours supprimé", "success")
    return redirect(url_for("courses.index"))