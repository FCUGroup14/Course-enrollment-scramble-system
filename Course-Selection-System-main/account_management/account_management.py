from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils import create_student_courses_file, load_accounts, save_accounts
import json
import os

account_mgmt_bp = Blueprint('account_management', __name__, template_folder='templates')

# ---------------------------- 帳號管裡主程式 ----------------------------
@account_mgmt_bp.route('/')
def index():
    accounts = load_accounts()
    return render_template('account_management/account_management.html', accounts=accounts)

@account_mgmt_bp.route('/register', methods=['POST'])
def register():
    data = request.form
    role = data.get('role')
    id = data.get('id')

    accounts = load_accounts()
    if any(acc['id'] == id for acc in accounts):  # ID already exists
        flash('這個 ID 已經存在，請使用其他 ID。', 'danger')
        return redirect(url_for('account_management.index'))

    new_account = {
        "id": id,
        "name": data.get('name'),
        "role": role,
        "password": data.get('password')
    }
    if role in ['學生', '系辦助教', '教授', '教務處人員']:  # 如果是學生或教職員，可以設置系級
        new_account["department"] = data.get('department')

    accounts.append(new_account)
    save_accounts(accounts)

    if role == '學生':
        create_student_courses_file(id)
    
    return redirect(url_for('account_management.index'))

@account_mgmt_bp.route('/delete/<account_id>', methods=['POST'])
def delete(account_id):
    accounts = load_accounts()
    
    # 找到被刪除帳號
    account_to_delete = next((acc for acc in accounts if acc['id'] == account_id), None)

    if account_to_delete:
        # 如果帳號是學生，刪除學生的課程檔案
        if account_to_delete['role'] == '學生':
            student_courses_file = f'database/student_data/{account_id}_courses.json'
            if os.path.exists(student_courses_file):
                os.remove(student_courses_file)
        
        # 如果帳號是教授，刪除該教授開設的課程，並從所有學生課程中移除相關課程
        elif account_to_delete['role'] == '教授':
            professor_name = account_to_delete['name']
            course_file = 'database/course.json'

            # 更新 course.json，刪除該教授的課程
            if os.path.exists(course_file):
                with open(course_file, 'r', encoding='utf-8') as f:
                    course_data = json.load(f)

                # 過濾掉該教授的課程
                updated_courses = [course for course in course_data if course.get('instructor') != professor_name]

                # 儲存更新後的課程檔案
                with open(course_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_courses, f, indent=4, ensure_ascii=False)

                # 遍歷所有學生檔案，刪除學生的相關課程
                student_data_dir = 'database/student_data'
                for student_file in os.listdir(student_data_dir):
                    if student_file.endswith('_courses.json'):
                        student_file_path = os.path.join(student_data_dir, student_file)
                        with open(student_file_path, 'r', encoding='utf-8') as f:
                            student_data = json.load(f)
                        
                        # 確保學生課程資料是字典格式
                        if isinstance(student_data, dict) and 'courses' in student_data:
                            # 更新課程列表
                            updated_student_courses = [
                                course for course in student_data['courses']
                                if not (isinstance(course, dict) and course.get('instructor') == professor_name)
                            ]
                            student_data['courses'] = updated_student_courses
                        else:
                            # 如果資料格式不正確，跳過該文件
                            continue
                        
                        # 儲存更新後的學生課程檔案
                        with open(student_file_path, 'w', encoding='utf-8') as f:
                            json.dump(student_data, f, indent=4, ensure_ascii=False)

        # 刪除帳號
        accounts = [acc for acc in accounts if acc['id'] != account_id]
        save_accounts(accounts)

        flash('帳號已成功刪除！', 'success')
    else:
        flash('找不到該帳號，無法刪除！', 'danger')
    
    return redirect(url_for('account_management.index'))

@account_mgmt_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    accounts = load_accounts()
    filtered_accounts = [acc for acc in accounts if query.lower() in acc['id'].lower()]
    return render_template('account_management/account_management.html', accounts=filtered_accounts)
