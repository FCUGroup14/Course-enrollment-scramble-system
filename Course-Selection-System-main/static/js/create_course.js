function validateForm() {
    const errors = [];
    
    const courseName = document.getElementById('course_name').value.trim();
    const courseDescription = document.getElementById('course_description').value.trim();
    const courseLocation = document.getElementById('course_location').value.trim();
    const maxStudents = document.getElementById('max_students').value;
    const credits = document.getElementById('credits').value;
    const selectedPeriods = document.querySelectorAll('input[name^="day_of_week"]:checked');

    if (courseName === '') {
        errors.push("課程名稱為必填！");
    } else if (courseName.length > 50) {
        errors.push("課程名稱不能超過50字！");
    }

    if (courseDescription === '') {
        errors.push("課程大綱為必填！");
    } else if (courseDescription.length > 200) {
        errors.push("課程大綱不能超過200字！");
    }

    if (credits==='') {
        errors.push("學分數為必填！");
    } else if (credits<0 || credits>10) {
        errors.push("學分數請輸入0-10學分之間!");
    }

    if (courseLocation === '') {
        errors.push("地點為必填！");
    } else if (courseLocation.length > 20) {
        errors.push("地點不能超過20字！");
    }

    if (maxStudents === '') {
        errors.push("選課人數上限為必填！");
    } else if (maxStudents < 5 || maxStudents > 250) {
        errors.push("選課人數上限應在5到250人之間！");
    }

    if (selectedPeriods.length === 0) {
        errors.push("請至少選擇一個課程時間！");
    }

    if (errors.length > 0) {
        alert(errors.join("\n"));  // 顯示所有錯誤訊息
        return false;
    }

    return confirm("確認送出?");
}
