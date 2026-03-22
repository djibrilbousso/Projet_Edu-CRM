from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils import login_required, is_valid_email
from app.services.teacher_service import add_teacher, list_teachers, delete_teacher

teachers = Blueprint("teachers", __name__, url_prefix="/teachers")

@teachers.route("/")
@login_required
def teachers_list():
    all_teachers = list_teachers()
    return render_template("teachers/list.html", teachers=all_teachers)

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
            flash("Email invalide - format requis: exemple@domaine.com", "danger")
            return redirect(url_for("teachers.teachers_add"))
        
        result = add_teacher(name, email, speciality)
        if result is None:
            flash("Cet email existe déjà", "danger")
            return redirect(url_for("teachers.teachers_add"))
        
        flash("Enseignant ajouté", "success")
        return redirect(url_for("teachers.teachers_list"))
    
    return render_template("teachers/add.html")

@teachers.route("/delete/<int:id>", methods=["POST"])
@login_required
def teachers_delete(id):
    delete_teacher(id)
    flash("Enseignant supprimé", "success")
    return redirect(url_for("teachers.teachers_list"))