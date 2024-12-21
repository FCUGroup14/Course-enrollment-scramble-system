// 提示框訊息
document.addEventListener("DOMContentLoaded", () => {
    const flashMessages = document.querySelectorAll("#error-message");

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
