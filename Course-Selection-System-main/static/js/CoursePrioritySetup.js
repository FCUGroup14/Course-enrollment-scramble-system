import React, { useState, useEffect } from 'react';
import { AlertCircle, Search, XCircle } from 'lucide-react';

const CoursePrioritySetup = () => {
    const [courses, setCourses] = useState([]);
    const [selectedCourses, setSelectedCourses] = useState([]);
    const [error, setError] = useState('');
    const [searchInput, setSearchInput] = useState('');
    const [directInput, setDirectInput] = useState('');

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await fetch('/api/courses');
                if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
                const data = await response.json();
                setCourses(data);
            } catch (error) {
                console.error('Error loading courses:', error);
                setError('無法讀取課程數據');
            }
        };
        fetchCourses();
    }, []);

    const filteredCourses = courses.filter(course => {
        const searchTerm = searchInput.toLowerCase();
        return (
            course.course_id.toLowerCase().includes(searchTerm) ||
            course.course_name.toLowerCase().includes(searchTerm) ||
            course.instructor.toLowerCase().includes(searchTerm)
        );
    });

    const handleDirectAdd = () => {
        if (!directInput) {
            setError('請輸入課程代碼或教師姓名');
            return;
        }

        const foundCourse = courses.find(
            course =>
                course.course_id === directInput ||
                course.instructor.includes(directInput)
        );

        if (foundCourse) {
            if (selectedCourses.some(c => c.course_id === foundCourse.course_id)) {
                setError('此課程已在清單中');
            } else {
                setSelectedCourses([...selectedCourses, foundCourse]);
                setDirectInput('');
                setError('');
            }
        } else {
            setError('找不到符合的課程');
        }
    };

    const addCourse = course => {
        if (selectedCourses.some(c => c.course_id === course.course_id)) {
            setError('此課程已在清單中');
            return;
        }
        setSelectedCourses([...selectedCourses, course]);
        setError('');
    };

    const removeCourse = courseId => {
        setSelectedCourses(selectedCourses.filter(c => c.course_id !== courseId));
    };

    const moveCourse = (fromIndex, toIndex) => {
        const newList = [...selectedCourses];
        const [movedItem] = newList.splice(fromIndex, 1);
        newList.splice(toIndex, 0, movedItem);
        setSelectedCourses(newList);
    };

    const savePriority = async () => {
        const courseIds = selectedCourses.map(course => course.course_id);
        try {
            const response = await fetch('/api/save-priority', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ priority: courseIds }),
            });
            if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
            alert('優先順序已保存！');
        } catch (error) {
            console.error('Error saving priority:', error);
            alert('保存失敗');
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-2xl font-bold mb-4">課程優先順序設定</h2>

                {error && (
                    <div className="flex items-center text-red-500 mb-4">
                        <AlertCircle className="w-5 h-5 mr-2" />
                        <span>{error}</span>
                    </div>
                )}

                <div className="mb-6">
                    <div className="flex gap-2">
                        <input
                            type="text"
                            value={directInput}
                            onChange={e => setDirectInput(e.target.value)}
                            placeholder="輸入課程代碼或教師姓名"
                            className="flex-1 p-2 border rounded"
                        />
                        <button
                            onClick={handleDirectAdd}
                            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                        >
                            新增
                        </button>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-6">
                    <div>
                        <div className="mb-3">
                            <div className="flex gap-2 items-center">
                                <Search className="w-5 h-5 text-gray-500" />
                                <input
                                    type="text"
                                    value={searchInput}
                                    onChange={e => setSearchInput(e.target.value)}
                                    placeholder="搜尋課程..."
                                    className="w-full p-2 border rounded"
                                />
                            </div>
                        </div>
                        <div className="h-96 overflow-y-auto border rounded">
                            {filteredCourses.map(course => (
                                <div
                                    key={course.course_id}
                                    className="p-3 hover:bg-gray-50 border-b cursor-pointer"
                                    onClick={() => addCourse(course)}
                                >
                                    <div className="font-medium">{course.course_name}</div>
                                    <div className="text-sm text-gray-500">
                                        課程代碼: {course.course_id} | 教師: {course.instructor} | 學分: {course.credits}
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div>
                        <h3 className="font-semibold mb-3">優先順序（由上至下）</h3>
                        <div className="h-96 overflow-y-auto border rounded">
                            {selectedCourses.map((course, index) => (
                                <div
                                    key={course.course_id}
                                    className="p-3 bg-white border-b flex items-center justify-between"
                                >
                                    <div className="flex-1">
                                        <div className="font-medium">{course.course_name}</div>
                                        <div className="text-sm text-gray-500">
                                            課程代碼: {course.course_id} | 教師: {course.instructor}
                                        </div>
                                    </div>
                                    <div className="flex gap-2">
                                        {index > 0 && (
                                            <button
                                                onClick={() => moveCourse(index, index - 1)}
                                                className="p-1 text-gray-500 hover:text-gray-700"
                                            >
                                                ↑
                                            </button>
                                        )}
                                        {index < selectedCourses.length - 1 && (
                                            <button
                                                onClick={() => moveCourse(index, index + 1)}
                                                className="p-1 text-gray-500 hover:text-gray-700"
                                            >
                                                ↓
                                            </button>
                                        )}
                                        <button
                                            onClick={() => removeCourse(course.course_id)}
                                            className="p-1 text-red-500 hover:text-red-700"
                                        >
                                            <XCircle className="w-5 h-5" />
                                        </button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="mt-6 flex justify-end">
                    <button
                        onClick={savePriority}
                        disabled={selectedCourses.length === 0}
                        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300"
                    >
                        儲存優先順序
                    </button>
                </div>
            </div>
        </div>
    );
};

export default CoursePrioritySetup.js;
