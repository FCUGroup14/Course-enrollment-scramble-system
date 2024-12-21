# 此部分放置退選需要用到的函式
from flask import flash, redirect, url_for
from utils import load_courses, load_student_courses, save_courses, save_student_courses

def drop_course(id, course_id):
    courses = load_courses()
    student_courses = load_student_courses(id)

    course = next((c for c in courses if c['course_id'] == course_id), None)

    if course:
        selected_course = next((c for c in student_courses if c['course_id'] == course_id), None)
        if selected_course:
            student_courses.remove(selected_course)

            course['act_students'] -= 1

            save_student_courses(id, {"courses": student_courses})
            save_courses(courses)

    return redirect(url_for('student_list.student_courses', id=id))
