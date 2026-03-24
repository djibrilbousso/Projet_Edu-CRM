teachers = []


def list_teachers():
    return teachers


def get_teacher_by_id(teacher_id):
    for t in teachers:
        if t["id"] == teacher_id:
            return t
    return None


def add_teacher(name, email, speciality):
    for t in teachers:
        if t["email"] == email:
            return None
    new_id = teachers[-1]["id"] + 1 if teachers else 1
    teacher = {"id": new_id, "name": name, "email": email, "speciality": speciality}
    teachers.append(teacher)
    return teacher


def update_teacher(teacher_id, name, email, speciality):
    from app.services.course_service import list_courses

    for t in teachers:
        if t["id"] == teacher_id:
            # Vérifier si la spécialité change et si l'enseignant a des cours
            if t["speciality"] != speciality:
                for c in list_courses():
                    if c["teacher_id"] == teacher_id:
                        return "has_courses"
            t["name"] = name
            t["email"] = email
            t["speciality"] = speciality
            return t
    return False


def search_teachers(query):
    query = query.strip().lower()
    results = []
    for t in teachers:
        if query in t["name"].lower():
            results.append(t)
    return results

def delete_teacher(teacher_id):
    from app.services.course_service import list_courses
    
    # Vérifier si l'enseignant a des cours
    for c in list_courses():
        if c["teacher_id"] == teacher_id:
            return False
    
    for t in teachers:
        if t["id"] == teacher_id:
            teachers.remove(t)
            return True
    return False