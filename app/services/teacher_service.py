teachers = []

def list_teachers():
    return teachers

def add_teacher(name, email, speciality):
    # Vérifier si l'email existe déjà
    for t in teachers:
        if t["email"] == email:
            return None
    
    # Créer l'ID
    if teachers:
        new_id = teachers[-1]["id"] + 1
    else:
        new_id = 1
    
    teacher = {"id": new_id, "name": name, "email": email, "speciality": speciality}
    teachers.append(teacher)
    return teacher

def get_teacher_by_id(teacher_id):
    for t in teachers:
        if t["id"] == teacher_id:
            return t
    return None

def delete_teacher(teacher_id):
    for t in teachers:
        if t["id"] == teacher_id:
            teachers.remove(t)
            return True
    return False