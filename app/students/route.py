from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.student_service import add_student, list_students, delete_student
from app.utils import login_required, is_valid_email

students_bp = Blueprint("students", __name__, url_prefix="/students")

@students_bp.route("/")
@login_required
def index():
    students = list_students()
    return render_template("students/list.html", students=students)

@students_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        
        if not name or not email:
            flash("Tous les champs sont obligatoires", "danger")
            return redirect(url_for("students.create"))
        
        if not is_valid_email(email):
            flash("Email invalide - format requis: halimalena@gmail.com", "danger")
            return redirect(url_for("students.create"))
        
        result = add_student(name, email)
        if result is None:
            flash("Cet email existe déjà", "danger")
            return redirect(url_for("students.create"))
        
        flash("Étudiant ajouté avec succès", "success")
        return redirect(url_for("students.index"))
    
    return render_template("students/create.html")

@students_bp.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    delete_student(id)
    flash("Étudiant supprimé", "success")
    return redirect(url_for("students.index"))