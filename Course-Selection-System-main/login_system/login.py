from flask import Blueprint, render_template, request, redirect, session, url_for
from account_management.account_management import load_accounts

login_bp = Blueprint('login', __name__, template_folder='templates')
    
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['id']
        password = request.form['password']
        accounts = load_accounts()

        # 比對 id 和 password
        for account in accounts:
            if account['id'] == user_id and account['password'] == password:
                if account['role'] == '學生':
                    return redirect(url_for('student_course.student_page', id=user_id))
                elif account['role'] == '系辦助教':
                    return redirect(url_for('student_list.student_list', id=user_id))
                elif account['role'] == '教授':
                    return redirect(url_for('create_course.home', id=user_id))
                elif account['role'] == '教務處人員':
                    return redirect(url_for('course_list.course_list', id=user_id))
        return render_template('login_system/login.html', error="帳號或密碼錯誤")
    return render_template('login_system/login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))