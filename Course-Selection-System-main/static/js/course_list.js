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

        // 重新載入所有課程
        const searchForm = document.getElementById("searchForm");
        searchForm.action = window.location.pathname;
        searchForm.submit();
    });
});