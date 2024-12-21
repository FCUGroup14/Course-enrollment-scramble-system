from flask import Blueprint, redirect, render_template, request, session, url_for
from account_management.account_management import load_accounts
from .search_course import filter_courses
from utils import load_courses, load_student_courses
from .add_course import add_course
from .drop_course import drop_course

student_course_bp = Blueprint('student_course', __name__, template_folder='templates')

# -------------------------------- 選課頁面 --------------------------------
@student_course_bp.route('/id=<id>')
def student_page(id):
    accounts = load_accounts()
    student = next((acc for acc in accounts if acc['id'] == id), None)
    session['student_id'] = id

    student_courses = load_student_courses(id)
    selected_course_ids = [course['course_id'] for course in student_courses]
    total_credits = calculate_total_credits(student_courses)

    # 載入所有課程資料
    courses = load_courses()

    # 過濾掉狀態為 "已停開" 的課程
    available_courses = [course for course in courses if course['status'] != '已停開']

    # 取得查詢條件
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    instructor = request.args.get('instructor')
    location = request.args.get('location')
    day_of_week = request.args.get('day_of_week')
    time_slot = request.args.get('time_slot')

    # 使用篩選函式過濾課程
    filtered_courses = filter_courses(
        available_courses,
        course_id=course_id,
        course_name=course_name,
        instructor=instructor,
        location=location,
        day_of_week=day_of_week,
        time_slot=time_slot
    )

    # 分頁處理，每頁顯示 10 項
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_courses = filtered_courses[start:end]
    
    # 計算總頁數
    total_pages = (len(filtered_courses) // per_page) + (1 if len(filtered_courses) % per_page > 0 else 0)

    # 傳遞資料到前端，包含所有課程
    return render_template('student_course/student.html', 
                           student=student, 
                           student_courses=student_courses, 
                           courses=paginated_courses,  # 開課的課程
                           all_courses=courses,  # 所有課程，包含已停開課程
                           page=page, 
                           total_pages=total_pages, 
                           selected_course_ids=selected_course_ids, 
                           total_credits=total_credits)



# -------------------------------- 加選功能 --------------------------------
@student_course_bp.route('/add_course/<id>/<course_id>', methods=['POST'])
def add_course_page(id, course_id):
    page = request.form.get('page', 1, type=int)
    add_course(id, course_id)
    return redirect(url_for('student_course.student_page', id=id, page=page))

# -------------------------------- 退選功能 --------------------------------
@student_course_bp.route('/drop_course/<id>/<course_id>', methods=['POST'])
def drop_course_page(id, course_id):
    page = request.form.get('page', 1, type=int)
    drop_course(id, course_id)
    return redirect(url_for('student_course.student_page', id=id, page=page))

# -------------------------------- 計算總學分 --------------------------------
def calculate_total_credits(student_courses):
    total_credits = sum(course['credits'] for course in student_courses)
    return total_credits
