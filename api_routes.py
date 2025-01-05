# api_routes.py
from flask import Blueprint, jsonify, request
import json

api_bp = Blueprint('api', __name__)

@api_bp.route('/courses')
def get_courses():
    try:
        with open('course.json', 'r', encoding='utf-8') as f:
            courses = json.load(f)
        return jsonify(courses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/save-priority', methods=['POST'])
def save_priority():
    try:
        data = request.get_json()
        with open('priority.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return jsonify({"message": "優先順序已保存"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
