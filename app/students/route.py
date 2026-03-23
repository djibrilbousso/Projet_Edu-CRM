from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils import login_required, is_valid_email, paginate
from app.services.student_service import add_student, list_students, delete_student, update_student, get_student_by_id

students_bp = Blueprint("students", __name__, url_prefix="/students")


@students_bp.route("/")
@login_required
def index():
    query = request.args.get("q", "").strip()
    niveau = request.args.get("niveau", "").strip()
    filiere = request.args.get("filiere", "").strip()

    all_students = list_students()
    results = []

    for s in all_students:
        if query and query.lower() not in s["name"].lower():
            continue
        if niveau and s["niveau"] != niveau:
            continue
        if filiere and s["filiere"] != filiere:
            continue
        results.append(s)

    page = request.args.get("page", 1, type=int)
    students_page, total_pages = paginate(results, page)

    url_pagination = url_for('students.index', q=query, niveau=niveau, filiere=filiere)
    return render_template("students/list.html", students=students_page, query=query,
                           page=page, total_pages=total_pages, url_pagination=url_pagination)


@students_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        niveau = request.form.get("niveau")
        filiere = request.form.get("filiere")

        if not name or not email or not niveau or not filiere:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("students.create"))

        if not is_valid_email(email):
            flash("Email invalide", "danger")
            return redirect(url_for("students.create"))

        result = add_student(name, email, niveau, filiere)
        if result is None:
            flash("Cet email existe déjà", "danger")
            return redirect(url_for("students.create"))

        flash("Étudiant ajouté avec succès", "success")
        return redirect(url_for("students.index"))

    return render_template("students/create.html")


@students_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    student = get_student_by_id(id)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        niveau = request.form.get("niveau")
        filiere = request.form.get("filiere")

        if not name or not email or not niveau or not filiere:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("students.edit", id=id))

        if not is_valid_email(email):
            flash("Email invalide", "danger")
            return redirect(url_for("students.edit", id=id))

        update_student(id, name, email, niveau, filiere)
        flash("Étudiant modifié avec succès", "success")
        return redirect(url_for("students.index"))

    return render_template("students/edit.html", student=student)


@students_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    delete_student(id)
    flash("Étudiant supprimé", "success")
    return redirect(url_for("students.index"))