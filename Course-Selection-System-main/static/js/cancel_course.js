function cancel_course(course_id) {
    if (confirm(`確定要停開課程 ${course_id} 嗎？`)) {
        fetch(`/course_list/cancel_course/course_id=${course_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ course_id: course_id })
        })
            .then(response => {
                if (response.ok) {
                    alert('停開成功！');
                    location.reload(); // 重新載入頁面
                } else {
                    response.json().then(data => alert(data.message || '停開失敗！'));
                }
            })
            .catch(error => console.error('停開錯誤:', error));
    }
}


function remove_course(course_id) {
    if (confirm(`確定要移除課程 ${course_id} 嗎？`)) {
        fetch(`/course_list/remove_course/course_id=${course_id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ course_id: course_id })
        })
            .then(response => {
                if (response.ok) {
                    alert('課程已移除！');
                    location.reload(); // 重新載入頁面
                } else {
                    response.json().then(data => alert(data.message || '移除失敗！'));
                }
            })
            .catch(error => console.error('移除錯誤:', error));
    }
}