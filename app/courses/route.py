from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.course_service import add_course, list_courses, delete_course, assign_student_to_course, get_course_by_id
from app.services.teacher_service import list_teachers
from app.services.student_service import list_students
from app.utils import login_required, paginate

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


@courses_bp.route("/")
@login_required
def index():
    all_courses = list_courses()
    all_teachers = list_teachers()
    
    # Créer un dictionnaire id -> nom pour accès rapide
    teachers_dict = {}
    for t in all_teachers:
        teachers_dict[t["id"]] = t["name"]
    
    page = request.args.get("page", 1, type=int)
    courses_page, total_pages = paginate(all_courses, page)
    url_pagination = url_for('courses.index')
    return render_template("courses/list.html",
                           courses=courses_page,
                           teachers_dict=teachers_dict,
                           page=page,
                           total_pages=total_pages,
                           url_pagination=url_pagination)

@courses_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    all_teachers = list_teachers()
    speciality = request.args.get("speciality", "")

    # Filtrer enseignants par spécialité
    if speciality:
        teachers = [t for t in all_teachers if t["speciality"] == speciality]
    else:
        teachers = []

    if request.method == "POST":
        title = request.form.get("title")
        teacher_id = request.form.get("teacher_id")
        speciality = request.form.get("speciality")

        if not title or not teacher_id or not speciality:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("courses.create"))

        result = add_course(title, int(teacher_id), speciality)
        if result is None:
            flash("Ce cours existe déjà", "danger")
            return redirect(url_for("courses.create"))
        if result is False:
            flash("Enseignant non trouvé", "danger")
            return redirect(url_for("courses.create"))

        flash("Cours ajouté avec succès", "success")
        return redirect(url_for("courses.index"))

    return render_template("courses/create.html",
                           teachers=teachers,
                           speciality=speciality)

@courses_bp.route("/assign/<int:course_id>", methods=["GET", "POST"])
@login_required
def assign(course_id):
    course = get_course_by_id(course_id)
    
    
    niveau = request.args.get("niveau", "")
    filiere = request.args.get("filiere", "")
    
    all_students = list_students()
    students = []
    for s in all_students:
        if niveau and s["niveau"] != niveau:
            continue
        if filiere and s["filiere"] != filiere:
            continue
        students.append(s)

    if request.method == "POST":
        student_id = request.form.get("student_id")

        if not student_id:
            flash("Veuillez choisir un étudiant", "danger")
            return redirect(url_for("courses.assign", course_id=course_id))

        result = assign_student_to_course(course_id, int(student_id))
        if result is None:
            flash("Cet étudiant est déjà inscrit", "danger")
            return redirect(url_for("courses.assign", course_id=course_id))
        if result is False:
            flash("Cours ou étudiant introuvable", "danger")
            return redirect(url_for("courses.assign", course_id=course_id))

        flash("Étudiant inscrit avec succès", "success")
        return redirect(url_for("courses.index"))

    return render_template("courses/assign.html",
                           course=course,
                           students=students,
                           niveau=niveau,
                           filiere=filiere)

@courses_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):

    delete_course(id)
    flash("Cours supprimé", "success")
    return redirect(url_for("courses.index"))


@courses_bp.route("/detail/<int:course_id>")
@login_required
def detail(course_id):
    course = get_course_by_id(course_id)
    all_students = list_students()
    
    # Récupérer les étudiants inscrits
    etudiants_inscrits = []
    for s in all_students:
        if s["id"] in course["student_ids"]:
            etudiants_inscrits.append(s)
    
    # Récupérer l'enseignant
    from app.services.teacher_service import get_teacher_by_id
    teacher = get_teacher_by_id(course["teacher_id"])

    page = request.args.get("page", 1, type=int)
    total_inscrits = len(etudiants_inscrits)
    etudiants_page, total_pages = paginate(etudiants_inscrits, page)
    url_pagination = url_for('courses.detail', course_id=course_id)

    return render_template("courses/detail.html",
                           course=course,
                           etudiants_inscrits=etudiants_page,
                           total_inscrits=total_inscrits,
                           teacher=teacher,
                           page=page,
                           total_pages=total_pages,
                           url_pagination=url_pagination)