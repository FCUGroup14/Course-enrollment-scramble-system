from flask import Blueprint, render_template, request, redirect, session, url_for
from account_management.account_management import load_accounts
from student_course.search_course import filter_courses
from utils import load_courses, load_student_courses
from .add import add_course
from .drop import drop_course

student_list_bp = Blueprint('student_list', __name__, template_folder='templates')

# 學生清單頁面
@student_list_bp.route('/student_list/id=<id>', methods=['GET'])
def student_list(id):
    query = request.args.get('query', '').strip()  # 搜索框的內容
    accounts = load_accounts()  # 加載所有賬戶

    assistant = next((acc for acc in accounts if acc['id'] == id), None)
    session['assistant_id'] = id

    # 過濾出角色為學生的賬戶（學生的ID以 'D' 開頭）
    students = [acc for acc in accounts if acc['id'].startswith('D')] 

    # 查詢ID或姓名
    if query:
        students = [
            acc for acc in students
            if query.lower() in acc['id'].lower() or query.lower() in acc['name'].lower()
        ]

    return render_template('student_list/student_list.html', students=students, assistant=assistant)



@student_list_bp.route('/student_list/student_courses/id=<id>')
def student_courses(id):
    accounts = load_accounts()
    student = next((acc for acc in accounts if acc['id'] == id), None)
    assistant = next((acc for acc in accounts if acc['id'].startswith('T')), None)

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

    # 使用篩選函式過濾課程
    filtered_courses = filter_courses(
        available_courses,
        course_id=course_id,
        course_name=course_name,
        instructor=instructor
    )

    return render_template('student_list/student_page.html', student=student, student_courses=student_courses, courses=filtered_courses, selected_course_ids=selected_course_ids, total_credits=total_credits, assistant=assistant)

# -------------------------------- 加選功能 --------------------------------
@student_list_bp.route('/add_course/<id>/<course_id>', methods=['POST'])
def add_course_page(id, course_id):
    add_course(id, course_id)
    return redirect(url_for('student_list.student_courses', id=id))

# -------------------------------- 退選功能 --------------------------------
@student_list_bp.route('/drop_course/<id>/<course_id>', methods=['POST'])
def drop_course_page(id, course_id):
    drop_course(id, course_id)
    return redirect(url_for('student_list.student_courses', id=id))

# -------------------------------- 計算總學分 --------------------------------
def calculate_total_credits(student_courses):
    total_credits = sum(course['credits'] for course in student_courses)
    return total_credits
