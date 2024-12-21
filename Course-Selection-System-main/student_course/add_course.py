# 此部分放置加選函式
from flask import flash, redirect, url_for
from utils import load_courses, load_student_courses, save_courses, save_student_courses
from .total_credits import calculate_total_credits

def add_course(id, course_id):
    courses = load_courses()  # 載入所有課程
    student_courses = load_student_courses(id)  # 載入當前學生已選課程

    # 查找對應課程
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if course:
        # 檢查是否已選此課程
        if not any(c['course_id'] == course['course_id'] for c in student_courses):
            if course['act_students'] < course['max_students']:
                # 計算加選後的總學分
                total_credits = calculate_total_credits(student_courses) + course['credits']
                
                # 檢查總學分是否超過 25
                if total_credits > 25:
                    flash("加選後超過 25 學分，無法加選此課程！")
                    return redirect(url_for('student_course.student_page', id=id))

                # 只儲存必要的欄位 (課程代碼, 名稱, 必選修, 學分, 教授)
                selected_course = {
                    "course_id": course['course_id'],
                    "name": course['course_name'],
                    "compulsory": course['compulsory'],
                    "credits": course['credits'],
                    "instructor": course['instructor']
                }
                student_courses.append(selected_course)

                # 更新課程的已選人數
                course['act_students'] += 1
                save_student_courses(id, {"courses": student_courses})  # 儲存學生的選課資料
                save_courses(courses)  # 儲存課程的選擇人數
                flash(f"成功加選課程：{course['course_name']}")
            else:
                flash("課程名額已滿！")
        else:
            flash("您已選過此課程！")
    else:
        flash("課程不存在！")

    return redirect(url_for('student_course.student_page', id=id))