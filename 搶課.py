from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoAlertPresentException

# 使用者輸入帳號、密碼和課程代碼
user_account = input("請輸入你的帳號: ")
user_password = input("請輸入你的密碼: ")
course_id = input("請輸入你想加選的課程代碼: ")

# 設定 WebDriver
driver = webdriver.Chrome()

def handle_and_get_alert():
    try:
        wait = WebDriverWait(driver, 5)
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print(f"Alert 內容: '{alert_text}'")
        alert.accept()
        return alert_text
    except (TimeoutException, NoAlertPresentException):
        print("沒有找到 alert")
        return None

try:
    # 開啟本機選課系統
    driver.get("http://127.0.0.1:5000/")

    # 設定等待器
    wait = WebDriverWait(driver, 10)

    # 模擬操作：輸入帳號密碼並登入
    username_input = driver.find_element(By.NAME, "id")
    password_input = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_input.send_keys(user_account)
    password_input.send_keys(user_password)
    login_button.click()

    time.sleep(2)  # 等待登入完成

    # 點擊 "查詢與選課" 按鈕
    search_choose = driver.find_element(By.ID, "nav-profile-2")
    if search_choose.get_attribute("aria-selected") == "false":
        search_choose.click()
        time.sleep(1)

    # 搜尋課程
    search_input = driver.find_element(By.NAME, "course_id")
    search_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")

    search_input.clear()  # 清除可能存在的文字
    search_input.send_keys(course_id)
    search_button.click()

    time.sleep(2)  # 等待搜尋結果

    # 找到並點擊餘額按鈕
    balance_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//tr[contains(., '{course_id}')]//button[contains(text(), '餘額')]")
    ))
    balance_button.click()

    # 處理並獲取餘額 alert 內容
    alert_text = handle_and_get_alert()
    
    if alert_text:
        try:
            # 解析餘額資訊
            available_slots0 = alert_text.split(':')[1].strip().split(' / ')[0]
            available_slots_int0 = int(available_slots0)
            available_slots1 = alert_text.split(':')[1].strip().split(' / ')[1]
            available_slots_int1 = int(available_slots1)

            if available_slots_int0 != available_slots_int1:
                time.sleep(1)  # 確保 alert 完全關閉
                
                # 重新找到目標課程的行
                course_row = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"//tr[contains(., '{course_id}')]")
                ))
                
                # 在該行中找到加選按鈕
                add_button = course_row.find_element(By.XPATH, ".//button[contains(text(), '加選')]")
                driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
                time.sleep(1)
                add_button.click()
                
                # 處理加選後的確認 alert
                result_text = handle_and_get_alert()
                if result_text:
                    print(f"加選結果: {result_text}")
            else:
                print(f"課程 {course_id} 名額不足")

        except ValueError:
            print(f"無法從 alert 內容中解析名額數字: '{alert_text}'，請檢查格式")
    else:
        print("無法獲取課程餘額信息")

    # 等待最後操作完成
    time.sleep(3)

finally:
    # 關閉瀏覽器
    driver.quit()