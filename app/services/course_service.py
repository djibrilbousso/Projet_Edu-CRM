from app.services import student_service, teacher_service

courses = []

def list_courses():
    return courses

def add_course(title, teacher_id):
    # Vérifier si le titre existe déjà
    for c in courses:
        if c["title"] == title:
            return None
    
    # Vérifier si l'enseignant existe
    teacher = teacher_service.get_teacher_by_id(teacher_id)
    if not teacher:
        return False
    
    # Créer l'ID
    if courses:
        new_id = courses[-1]["id"] + 1
    else:
        new_id = 1
    
    course = {"id": new_id, "title": title, "teacher_id": teacher_id, "student_ids": []}
    courses.append(course)
    return course

def delete_course(course_id):
    for c in courses:
        if c["id"] == course_id:
            courses.remove(c)
            return True
    return False