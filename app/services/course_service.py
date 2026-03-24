from app.services import student_service, teacher_service

courses = []


def list_courses():
    return courses


def get_course_by_id(course_id):
    for c in courses:
        if c["id"] == course_id:
            return c
    return None


def add_course(title, teacher_id, speciality):
    for c in courses:
        if c["title"] == title:
            return None

    teacher = teacher_service.get_teacher_by_id(teacher_id)
    if not teacher:
        return False

    new_id = courses[-1]["id"] + 1 if courses else 1
    course = {
        "id": new_id,
        "title": title,
        "teacher_id": teacher_id,
        "speciality": speciality,
        "student_ids": []
    }
    courses.append(course)
    return course

def assign_student_to_course(course_id, student_id):
    course = get_course_by_id(course_id)
    if not course:
        return False

    
    student = student_service.get_student_by_id(student_id)
    if not student:
        return False

    if student_id in course["student_ids"]:
        return None

    course["student_ids"].append(student_id)
    return course


def delete_course(course_id):
    for c in courses:
        if c["id"] == course_id:
            courses.remove(c)
            return True
    return False