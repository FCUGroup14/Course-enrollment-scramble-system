# 此部分放置退選需要用到的函式
from flask import flash, redirect, url_for
from utils import load_courses, load_student_courses, save_courses, save_student_courses
from .total_credits import calculate_total_credits

def drop_course(id, course_id):
    courses = load_courses()  # 載入所有課程
    student_courses = load_student_courses(id)  # 載入當前學生已選課程

    # 查找對應課程
    course = next((c for c in courses if c['course_id'] == course_id), None)

    if course:
        if course.get('compulsory') != '必修':
            # 檢查學生是否選過此課程
            selected_course = next((c for c in student_courses if c['course_id'] == course_id), None)
            if selected_course:
                # 移除選課清單中的該課程
                student_courses.remove(selected_course)

                # 計算退選後的總學分
                total_credits = calculate_total_credits(student_courses)
                
                # 檢查退選後總學分是否低於 9
                if total_credits < 9:
                    flash("退選後學分低於 9，無法退選此課程！")
                    return redirect(url_for('student_course.student_page', id=id))

                # 更新課程的已選人數
                course['act_students'] -= 1

                # 儲存更新後的選課資料
                save_student_courses(id, {"courses": student_courses})
                # 儲存更新後的課程資料
                save_courses(courses)
                flash(f"成功退選課程：{course['course_name']}")
            else:
                flash("您尚未選擇此課程！")
        else:
            flash("此為必修課程，請聯絡系辦助教退選！")
            return redirect(url_for('student_course.student_page', id=id))
    else:
        flash("課程不存在！")

    return redirect(url_for('student_course.student_page', id=id))
