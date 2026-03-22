students = []

def list_students():
    return students

def add_student(name, email):
   
    for s in students:
        if s["email"] == email:
            return None
    
   
    if students:
        new_id = students[-1]["id"] + 1
    else:
        new_id = 1
    
    student = {"id": new_id, "name": name, "email": email}
    students.append(student)
    return student

def get_student_by_id(student_id):
    for s in students:
        if s["id"] == student_id:
            return s
    return None

def delete_student(student_id):
    for s in students:
        if s["id"] == student_id:
            students.remove(s)
            return True
    return False