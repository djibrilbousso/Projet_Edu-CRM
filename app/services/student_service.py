students = []


def list_students():
    return students


def get_student_by_id(student_id):
    for s in students:
        if s["id"] == student_id:
            return s
    return None


def add_student(name, email, niveau, filiere):
    for s in students:
        if s["email"] == email:
            return None
    new_id = students[-1]["id"] + 1 if students else 1
    student = {
        "id": new_id,
        "name": name,
        "email": email,
        "niveau": niveau,
        "filiere": filiere
    }
    students.append(student)
    return student


def update_student(student_id, name, email, niveau, filiere):
    for s in students:
        if s["id"] == student_id:
            s["name"] = name
            s["email"] = email
            s["niveau"] = niveau
            s["filiere"] = filiere
            return s
    return False


def search_students(query):
    query = query.strip().lower()
    results = []
    for s in students:
        if query in s["name"].lower() or query in s["niveau"].lower() or query in s["filiere"].lower():
            results.append(s)
    return results


def delete_student(student_id):
    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            return True
    return False