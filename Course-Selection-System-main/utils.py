# 這裡放置載入、刪除課程等函式
import json
from collections import OrderedDict # 使用該模組固定json字典順序
import os

# 載入所有帳號
def load_accounts():
    try:
        with open('database/accounts.json', 'r', encoding='utf-8') as file:
            accounts = json.load(file)
    except FileNotFoundError:
        accounts = []
    return accounts

# 儲存所有帳號
def save_accounts(accounts):
    with open('database/accounts.json', 'w', encoding='utf-8') as f:
        json.dump(accounts, f, indent=4, ensure_ascii=False)

# 建立學生課程檔案
def create_student_courses_file(id):
    # 確保資料夾存在
    folder_path = 'database/student_data'
    os.makedirs(folder_path, exist_ok=True)
    
    # 學生課程檔案路徑
    file_path = os.path.join(folder_path, f"{id}_courses.json")
    
    # 預設的課程資料結構
    default_courses = {
        "courses": []
    }
    
    # 保存 JSON 檔案
    with open(file_path, 'w') as f:
        json.dump(default_courses, f, indent=4)

# 載入所有課程
def load_courses(): 
    course_file = "database/course.json"
    try:
        with open(course_file, 'r', encoding='utf-8') as file:
            courses = json.load(file, object_pairs_hook=OrderedDict)
            return courses
    except FileNotFoundError:
        return []

# 載入學生課程
def load_student_courses(id):
    student_file = f"database/student_data/{id}_courses.json"
    try:
        with open(student_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 確保返回的是正確的格式
            return data.get('courses', [])
    except FileNotFoundError:
        return []  # 如果檔案不存在，返回空課程列表
    except json.JSONDecodeError:
        return []  # 如果 JSON 解析錯誤，也返回空課程列表
    
# 儲存所有課程
def save_courses(courses):
    course_file = "database/course.json"
    with open(course_file, 'w', encoding='utf-8') as file:
        json.dump(courses, file, ensure_ascii=False, indent=4)

# 儲存學生課程
def save_student_courses(id, student_courses):
    course_file = f"database/student_data/{id}_courses.json"
    with open(course_file, 'w', encoding='utf-8') as file:
        json.dump(student_courses, file, ensure_ascii=False, indent=4)

# 當停開後刪除學生資料庫中的課程資料。cancel_course 使用
def remove_course_from_all_students(course_id):
    # 取得學生課程資料檔案
    student_files = [f for f in os.listdir("database/student_data/") if f.endswith('_courses.json')]
    
    for student_file in student_files:
        student_course_file = os.path.join("database/student_data/", student_file)
        
        try:
            # 讀取學生的課程資料
            with open(student_course_file, 'r', encoding='utf-8') as file:
                student_data = json.load(file)
            
            # 刪除該課程
            updated_courses = [
                course for course in student_data.get('courses', []) if course.get('course_id') != course_id
            ]
            
            # 儲存更新後的課程資料
            with open(student_course_file, 'w', encoding='utf-8') as file:
                json.dump({'courses': updated_courses}, file, ensure_ascii=False, indent=4)
        
        except Exception as e:
            print(f"無法處理學生檔案 {student_file}: {str(e)}")