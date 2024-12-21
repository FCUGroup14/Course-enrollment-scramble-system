document.addEventListener("DOMContentLoaded", () => {
    // 查詢按鈕的點擊事件
    document.querySelector(".btn-primary").addEventListener("click", () => {
        const searchForm = document.getElementById("searchForm");
        searchForm.submit();
    });

    // 清除按鈕的點擊事件
    document.querySelector(".btn-outline-secondary").addEventListener("click", () => {
        document.getElementById("course_id").value = "";
        document.getElementById("course_name").value = "";
        document.getElementById("instructor").value = "";
        document.getElementById("day_of_week").value = "";
        document.getElementById("time_slot").value = "";

        // 重新載入所有課程
        const searchForm = document.getElementById("searchForm");
        searchForm.action = window.location.pathname;
        searchForm.submit();
    });
});


// 提示框訊息
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll("#flash-message-1, #flash-message-2");

    flashMessages.forEach(flashMessage => {
        if (flashMessage) {
            setTimeout(() => {
                flashMessage.classList.remove("show");
                flashMessage.classList.add("fade");

                // 移除元素（在淡出後500毫秒）
                setTimeout(() => flashMessage.remove(), 500);
            }, 2000);
        }
    });
});
