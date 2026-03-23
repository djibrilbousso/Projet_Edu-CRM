from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils import login_required, is_valid_email, paginate
from app.services.teacher_service import add_teacher, list_teachers, delete_teacher, update_teacher, search_teachers, get_teacher_by_id

teachers = Blueprint("teachers", __name__, url_prefix="/teachers")


@teachers.route("/")
@login_required
def teachers_list():
    #query = request.args.get("q", "")
    query = request.args.get("q", "").strip()
    if query:
        all_teachers = search_teachers(query)
    else:
        all_teachers = list_teachers()

    page = request.args.get("page", 1, type=int)
    teachers_page, total_pages = paginate(all_teachers, page)

    url_pagination = url_for('teachers.teachers_list', q=query)
    return render_template("teachers/list.html", teachers=teachers_page, query=query,
                           page=page, total_pages=total_pages, url_pagination=url_pagination)


@teachers.route("/add", methods=["GET", "POST"])
@login_required
def teachers_add():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        if not name or not email or not speciality:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("teachers.teachers_add"))

        if not is_valid_email(email):
            flash("Email invalide", "danger")
            return redirect(url_for("teachers.teachers_add"))

        result = add_teacher(name, email, speciality)
        if result is None:
            flash("Cet email existe déjà", "danger")
            return redirect(url_for("teachers.teachers_add"))

        flash("Enseignant ajouté", "success")
        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/add.html")


@teachers.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def teachers_edit(id):
    teacher = get_teacher_by_id(id)

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        speciality = request.form.get("speciality")

        if not name or not email or not speciality:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("teachers.teachers_edit", id=id))

        if not is_valid_email(email):
            flash("Email invalide", "danger")
            return redirect(url_for("teachers.teachers_edit", id=id))

        update_teacher(id, name, email, speciality)
        flash("Enseignant modifié", "success")
        return redirect(url_for("teachers.teachers_list"))

    return render_template("teachers/edit.html", teacher=teacher)


@teachers.route("/delete/<int:id>", methods=["POST"])
@login_required
def teachers_delete(id):
    delete_teacher(id)
    flash("Enseignant supprimé", "success")
    return redirect(url_for("teachers.teachers_list"))