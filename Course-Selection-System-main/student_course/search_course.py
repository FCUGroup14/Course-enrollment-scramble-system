# 此部分放置搜尋需要用到的函式
def filter_courses(courses, course_id=None, course_name=None, instructor=None, location=None, day_of_week=None, time_slot=None, status=None):
    if not any([course_id, course_name, instructor, location, day_of_week, time_slot, status]):
        return courses  # 如果沒有任何查詢條件，返回所有課程

    filtered_courses = []
    for course in courses:
        if status and status not in course['status']:
            continue
        if course_id and course_id not in course['course_id']:
            continue
        if course_name and course_name not in course['course_name']:
            continue
        if instructor and instructor not in course['instructor']:
            continue
        if location and location not in course['location']:
            continue
        # 比對星期與節次
        if day_of_week or time_slot:
            # 從 day_of_week 中獲取指定星期的節次
            course_time_slots = course['day_of_week'].get(day_of_week, []) if day_of_week else []
            
            # 若有輸入 time_slot，將其轉為集合進行交集運算
            if time_slot:
                # 檢查時間節次是否匹配
                if time_slot not in course_time_slots:
                    continue
            else:
                # 若僅指定 day_of_week，但該天無任何課程
                if not course_time_slots:
                    continue

        filtered_courses.append(course)

    return filtered_courses
