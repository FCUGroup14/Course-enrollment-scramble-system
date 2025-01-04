from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException

# 使用者輸入帳號、密碼和課程代碼列表
user_account = input("請輸入你的帳號: ")
user_password = input("請輸入你的密碼: ")
course_ids = input("請輸入你想加選的課程代碼（多個代碼以逗號分隔）: ").split(',')
number_of_courses = len(course_ids)
count = 0

while True:
    invalid_codes = [course_id for course_id in course_ids if len(course_id.strip()) != 4 or not course_id.isdigit()]
    if invalid_codes:
        print(f"格式錯誤的課程代碼: {', '.join(invalid_codes)}")
        course_ids = input("請重新輸入你想加選的課程代碼（多個代碼以逗號分隔，需為4位數字）: ").split(',')
    else:
        number_of_courses = len(course_ids)
        break

# 設定 WebDriver
driver = webdriver.Chrome()

def check_flash_message():
    try:
        # 檢查頁面上是否有提示訊息
        flash_message = driver.find_element(By.CSS_SELECTOR, ".alert.alert-primary")
        message_text = flash_message.text
        if "加選後超過 25 學分，無法加選此課程！" in message_text:
            return True
    except NoSuchElementException:
        return False

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

    # 依次處理每個課程代碼
    while count < number_of_courses:
        for course_id in course_ids:
            #course_id = course_id.strip()  # 去除多餘的空白
            #print(f"正在處理課程代碼: {course_id}")

            # 搜尋課程
            search_input = driver.find_element(By.NAME, "course_id")
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='button']")

            search_input.clear()  # 清除可能存在的文字
            search_input.send_keys(course_id)
            search_button.click()

            time.sleep(2)  # 等待搜尋結果

            try:
                # 找到並點擊餘額按鈕
                balance_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//tr[contains(., '{course_id}')]//button[contains(text(), '餘額')]")
                ))
                balance_button.click()

                # 處理並獲取餘額 alert 內容
                alert_text = handle_and_get_alert()

                if alert_text:
                    # 解析餘額資訊
                    available_slots0 = alert_text.split(':')[1].strip().split(' / ')[0]
                    available_slots_int0 = int(available_slots0)
                    available_slots1 = alert_text.split(':')[1].strip().split(' / ')[1]
                    available_slots_int1 = int(available_slots1)

                    if available_slots_int0 < available_slots_int1:
                        time.sleep(1)  # 確保 alert 完全關閉

                        # 重新找到目標課程的行
                        course_row = wait.until(EC.presence_of_element_located(
                            (By.XPATH, f"//tr[contains(., '{course_id}')]")
                        ))

                        # 在該行中找到加選按鈕
                        add_button = course_row.find_element(By.XPATH, ".//button[text()='加選']")
                        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
                        time.sleep(1)

                        # 找到已選學分和每門課程的學分
                        #total_credits = course_row.find_element(By.CLASS_NAME, "total-credits").text
                        #total_credits = int(total_credits)  # 轉換成整數

                        #each_course_credits = course_row.find_element(By.CLASS_NAME, "course-credits").text
                        #each_course_credits = int(each_course_credits)  # 轉換成整數

                        # 檢查加選課程後的總學分是否超過25學分
                        #if total_credits + each_course_credits <= 25:
                        add_button.click()  # 點擊 "加選" 按鈕

                        # 檢查是否有學分已滿的提示訊息
                        if check_flash_message():
                            print(f"學分已滿")
                        else:
                            count += 1
                            print(f"課程 {course_id} 已成功加選")
                            

                    else:
                        print(f"課程 {course_id} 名額不足")

                else:
                    print(f"無法獲取課程 {course_id} 的餘額信息")

            except NoSuchElementException:
                print(f"課程 {course_id} 已加選")

            time.sleep(2)  # 等待下一次搜尋

finally:
    # 關閉瀏覽器
    driver.quit()
