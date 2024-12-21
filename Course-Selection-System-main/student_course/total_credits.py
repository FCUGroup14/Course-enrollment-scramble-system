def calculate_total_credits(student_courses):
    total_credits = sum(course['credits'] for course in student_courses)
    return total_credits