from app.services import student_service, teacher_service

courses = []
_next_id = 1

def list_courses():
    return courses

def add_course(title, teacher_id):
    global _next_id
    teacher = next((t for t in teacher_service.teachers if t['id'] == teacher_id), None)
    if not teacher:
        raise ValueError(f"Teacher {teacher_id} not found")
    course = {'id': _next_id, 'title': title, 'teacher_id': teacher_id, 'student_ids': []}
    courses.append(course)
    _next_id += 1
    return course

def assign_student_to_course(course_id, student_id):
    course = next((c for c in courses if c['id'] == course_id), None)
    if not course:
        raise ValueError(f"Course {course_id} not found")
    student = next((s for s in student_service.students if s['id'] == student_id), None)
    if not student:
        raise ValueError(f"Student {student_id} not found")
    if student_id not in course['student_ids']:
        course['student_ids'].append(student_id)
    return course

def delete_course(course_id):
    global courses
    courses = [c for c in courses if c['id'] != course_id]