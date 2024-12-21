# 此部分放置加選函式
from flask import flash, redirect, url_for
from utils import load_courses, load_student_courses, save_courses, save_student_courses

def add_course(id, course_id):
    courses = load_courses()
    student_courses = load_student_courses(id)

    course = next((c for c in courses if c['course_id'] == course_id), None)

    if course:
        if not any(c['course_id'] == course['course_id'] for c in student_courses):
            if course['act_students'] < course['max_students']:

                selected_course = {
                    "course_id": course['course_id'],
                    "name": course['course_name'],
                    "compulsory": course['compulsory'],
                    "credits": course['credits'],
                    "instructor": course['instructor']
                }
                student_courses.append(selected_course)

                course['act_students'] += 1

                save_student_courses(id, {"courses": student_courses})
                save_courses(courses)

    return redirect(url_for('student_list.student_courses', id=id))