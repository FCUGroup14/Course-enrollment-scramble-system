from flask import Blueprint, render_template, request, session, jsonify
from account_management.account_management import load_accounts
from student_course.search_course import filter_courses
from utils import load_courses, remove_course_from_all_students, save_courses

course_list_bp = Blueprint("course_list", __name__, template_folder="templates")

@course_list_bp.route("cancel_course/id=<id>")
def course_list(id):
    accounts = load_accounts()
    user = next((acc for acc in accounts if acc["id"] == id), None)
    session["admin_id"] = id

    courses = load_courses()


    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    status = request.args.get('status')

    # 使用篩選函式過濾課程
    filtered_courses = filter_courses(
        courses,
        course_id=course_id,
        course_name=course_name,
        status=status
    )

    # 分頁處理，每頁顯示 10 項
    page = request.args.get('page', 1, type=int)
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    paginated_courses = filtered_courses[start:end]
    
    # 計算總頁數
    total_pages = (len(filtered_courses) // per_page) + (1 if len(filtered_courses) % per_page > 0 else 0)

    return render_template("course_list/course_list.html", user=user, courses=paginated_courses, page=page, total_pages=total_pages)

# 刪除所有學生的課程資料中的該課程
@course_list_bp.route("/cancel_course/course_id=<course_id>", methods=["POST"])
def cancel_course(course_id):
    
    # 加載現有的課程資料，使用 OrderedDict
    courses = load_courses()

    # 找到要移除的課程
    course_to_update = None
    for course in courses:
        if course.get("course_id") == course_id:
            course_to_update = course
            break

    if course_to_update:
        # 更新課程狀態
        course_to_update["status"] = "已停開"

        try:
            save_courses(courses)
            remove_course_from_all_students(course_id)
            return jsonify({"message": "停開成功！", "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": f"寫入文件失敗: {str(e)}", "status": "error"}), 500
    else:
        return jsonify({"message": "停開失敗！課程代碼無效。", "status": "error"}), 400
    
@course_list_bp.route("/remove_course/course_id=<course_id>", methods=["POST"])
def remove_course(course_id):
    # 加載現有的課程資料
    courses = load_courses()

    # 找到對應的課程
    course_to_remove = None
    for course in courses:
        if course.get("course_id") == course_id:
            course_to_remove = course
            break

    if course_to_remove:
        # 移除課程
        courses.remove(course_to_remove)

        # 寫回 JSON 文件
        try:
            save_courses(courses)
            return jsonify({"message": "課程已移除！", "status": "success"}), 200
        except Exception as e:
            return jsonify({"message": f"寫入文件失敗: {str(e)}", "status": "error"}), 500
    else:
        return jsonify({"message": "移除失敗！課程代碼無效。", "status": "error"}), 400
