from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException

# 使用者輸入帳號、密碼和課程代碼
user_account = 'D1149279'
user_password = '1149279'
course_ids = ['1450', '2776','1433']  # 要選的課程清單
successfully_enrolled_courses = []  # 追蹤成功加選的課程

# 設定 WebDriver
driver = webdriver.Chrome()

def check_enrollment_failure(driver):
    try:
        # 使用更靈活的XPath選擇器來匹配錯誤訊息
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//div[contains(@class, 'alert-primary')]//p[normalize-space()]"
            ))
        )
        
        # 獲取錯誤訊息文本並去除首尾空白
        message_text = error_message.text.strip()
        print(f"檢測到錯誤訊息: {message_text}")
        
        # 檢查錯誤訊息是否包含學分超過的提示
        if '加選後超過 25 學分' in message_text:
            print("加選失敗: 學分數超過限制")
            return True
        else:
            print(f"其他錯誤訊息: {message_text}")
            return False
            
    except TimeoutException:
        print("等待錯誤訊息超時")
        return False
    except NoSuchElementException:
        print("未找到錯誤訊息元素")
        return False
    except Exception as e:
        print(f"發生未預期的錯誤: {str(e)}")
        return False

def click_element_safely(element, wait_time=10):
    try:
        wait = WebDriverWait(driver, wait_time)
        element = wait.until(EC.element_to_be_clickable(element))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        
        try:
            element.click()
        except Exception as e:
            try:
                driver.execute_script("arguments[0].click();", element)
            except Exception as e:
                try:
                    ActionChains(driver).move_to_element(element).click().perform()
                except Exception as e:
                    print(f"所有點擊方法都失敗: {str(e)}")
                    raise e
    except Exception as e:
        print(f"無法點擊元素: {str(e)}")
        raise e

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
def click_add_course_button(course_id):
    try:
        # 找到課程所在的行
        course_row = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//tr[contains(., '{course_id}')]")
        ))

        # 檢查是否已經有「退選」按鈕，表示已加選
        try:
            withdraw_button = course_row.find_element(By.XPATH, ".//button[text()='退選']")
            print(f"課程 {course_id} 已加選過，跳過此課程")
            return False  # 課程已加選，跳過
        except NoSuchElementException:
            pass  # 沒有找到「退選」按鈕，繼續處理

        # 檢查「加選」按鈕是否存在
        add_button = course_row.find_element(By.XPATH, ".//button[text()='加選']")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)  # 等待按鈕滾動完成

        # 點擊加選按鈕
        click_element_safely(add_button)
        return True
    except Exception as e:
        print(f"無法加選課程 {course_id}：{e}")
        return False
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

    # 點擊查詢與選課頁籤
    search_choose = wait.until(EC.presence_of_element_located((By.ID, "nav-profile-2")))

    search_choose.click()
    # 依次處理每個課程代碼

    while sorted(successfully_enrolled_courses) != sorted(course_ids):

        for course_id in course_ids:
            # 搜尋課程
        # 輸入課程代碼並執行搜尋
            course_id_input = wait.until(EC.presence_of_element_located((By.ID, "course_id")))
            search_button = wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "button.btn.btn-primary")
            ))
            
            course_id_input.clear()
            course_id_input.send_keys(course_id)
            click_element_safely(search_button)
            time.sleep(1)

            try:
                # 找到並點擊餘額按鈕
                balance_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//tr[contains(., '{course_id}')]//button[contains(text(), '餘額')]")
                ))
                click_element_safely(balance_button)

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

                      # 檢查是否已經加選過
                        if click_add_course_button(course_id):
                            if check_enrollment_failure(driver):
                                print(f"課程 {course_id} 加選失敗，超過學分限制")
                            else:
                                if not course_id in successfully_enrolled_courses :
                                    successfully_enrolled_courses.append(course_id)
                                print(f"課程 {course_id} 已成功加選")
                        else:
                            if not course_id in successfully_enrolled_courses :
                                successfully_enrolled_courses.append(course_id)
                            print(f"課程 {course_id} 已加選過了")
                    else:
                        print(f"課程 {course_id} 名額不足")

                else:
                    print(f"無法獲取課程 {course_id} 的餘額信息")

            except NoSuchElementException:
                if not course_id in successfully_enrolled_courses :
                    successfully_enrolled_courses.append(course_id)
                print(f"課程 {course_id} 已加選過了")

            print(f'目前已成功加選的課程: {successfully_enrolled_courses}')
            time.sleep(2)  # 等待下一次搜尋

finally:
    print(f'已成功加選的課程: {successfully_enrolled_courses}')
    print('搶課系統已完成所有課程之加選')
    # 關閉瀏覽器
    driver.quit()