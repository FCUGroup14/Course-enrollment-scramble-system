from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 使用者輸入帳號、密碼和課程代碼
user_account = input("請輸入你的帳號: ")
user_password = input("請輸入你的密碼: ")
course_id = input("請輸入你想加選的課程代碼: ")

# 設定 WebDriver
driver = webdriver.Chrome()  # 確保已安裝相符版本的 ChromeDriver

try:
    # 開啟本機選課系統
    driver.get("http://127.0.0.1:5000/")

    # 等待頁面加載完成
    time.sleep(2)

    # 模擬操作：輸入帳號密碼並登入
    username_input = driver.find_element(By.NAME, "id")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")


    username_input.send_keys(user_account)
    password_input.send_keys(user_password)
    login_button.click()

    # 等待登入完成
    time.sleep(2)

    # 模擬選課操作
    course_button = driver.find_element(By.XPATH, f"//button[@data-course-id='{course_id}']")
    course_button.click()

    # 等待操作完成
    time.sleep(2)

finally:
    # 關閉瀏覽器
    driver.quit()
