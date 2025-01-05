from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time

# 使用者輸入帳號、密碼和課程代碼
# user_account = 'D1149279'
# user_password = '1149279'
# course_ids = ['1433','1432','3626','1450','1400']  # 要選的課程清單
user_account = input("請輸入你的帳號: ")
user_password = input("請輸入你的密碼: ")
course_ids = input("請輸入你想加選的課程代碼（多個代碼以逗號分隔）: ").split(',')
print(course_ids)
successfully_enrolled_courses = []  # 追蹤成功加選的課程

while True:
    invalid_codes = [course_id for course_id in course_ids if len(course_id.strip()) != 4 or not course_id.isdigit()]
    if invalid_codes:
        print(f"格式錯誤的課程代碼: {', '.join(invalid_codes)}")
        course_ids = input("請重新輸入你想加選的課程代碼（多個代碼以逗號分隔，需為4位數字）: ").split(',')
    else:
        break
# 設定 WebDriver
driver = webdriver.Chrome()

def unenrollment(course_id):
    """
    Withdraws from previously enrolled courses with lower priority than the target course
    to make room for adding the new course.
    """
    try:
        # Get the index (priority) of the current course from course_ids
        current_priority = course_ids.index(course_id)
        
        # Find courses with lower priority
        lower_priority_courses = []
        for enrolled_course in successfully_enrolled_courses:
            enrolled_priority = course_ids.index(enrolled_course)
            if enrolled_priority > current_priority:
                lower_priority_courses.append((enrolled_course, enrolled_priority))
        
        if not lower_priority_courses:
            print(f"沒有優先權較低的課程可以退選")
            return False
            
        lower_priority_courses.sort(key=lambda x: x[1], reverse=True)
        #print(f"優先權較低的課程清單: {lower_priority_courses}")
        
        course_to_withdraw = lower_priority_courses[0][0]
        #print(f"準備退選課程: {course_to_withdraw}")
        
        # Search for the course
        course_id_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "course_id"))
        )
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary"))
        )
        
        course_id_input.clear()
        course_id_input.send_keys(course_to_withdraw)
        click_element_safely(search_button)
        time.sleep(1)
        
        try:
            # 找到包含退選按鈕的表單
            # WebDriverWait(driver, 5).until(
            #     EC.presence_of_element_located((By.XPATH, 
            #         f"//tr[.//td[normalize-space(text())='{course_to_withdraw}']]//button[text()='加選']"))
            # )
            form = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, 
                    f"//tr[.//td[normalize-space(text())='{course_to_withdraw}']]//form[.//button[contains(text(), '退選')]]"))
            )
            #print("找到退選表單")
            
            # 使用 JavaScript 提交表單
            driver.execute_script("""
                if(confirm('確定要退選此課程嗎？')) {
                    arguments[0].submit();
                }
                                 
            """, form)
            handle_and_get_alert()
            #print("已提交退選表單")

            time.sleep(1)  # 等待表單提交完成

            search(course_to_withdraw)
           
            time.sleep(1)
            
            # 檢查是否變成加選按鈕
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, 
                        f"//tr[.//td[normalize-space(text())='{course_to_withdraw}']]//button[text()='加選']"))
                )
                # 退選成功
                successfully_enrolled_courses.remove(course_to_withdraw)
                print(f"已成功退選課程 {course_to_withdraw}")
                print(f"目前已選課程: {successfully_enrolled_courses}")
                return True
                
            except TimeoutException:
                print("未檢測到退選成功的標誌（加選按鈕）")
                return False
            
        except Exception as e:
            print(f"退選操作失敗: {str(e)}")
            return False
            
    except Exception as e:
        print(f"退選過程發生錯誤: {str(e)}")
        return False
    
def check_enrollment_failure(driver):
    try:
        # 等待錯誤訊息出現
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "flash-message-2"),
                "加選後超過 25 學分"  # 部分錯誤訊息即可
            )
        )
        # 確認並打印錯誤訊息
        error_message_element = driver.find_element(By.ID, "flash-message-2")
        message_text = error_message_element.text.strip()
        
        # 檢查是否包含學分超過的提示
        if '加選後超過 25 學分' in message_text:
            #print("加選失敗: 學分數超過限制")
            # 等待訊息自動消失（因為有 2 秒自動消失的設定）
            time.sleep(2)
            return True
        else:
            print(f"其他錯誤訊息: {message_text}")
            time.sleep(2)  # 同樣等待訊息消失
            return False
            
    except TimeoutException:
        # print("未檢測到錯誤訊息")
        return False
    except NoSuchElementException:
        print("未找到錯誤訊息元素")
        return False
    except Exception as e:
        print(f"檢查選課狀態時發生錯誤: {str(e)}")
        return False

def click_element_safely(element, wait_time=10):
    try:
        wait = WebDriverWait(driver, wait_time)
        element = wait.until(EC.element_to_be_clickable(element))
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
        
        try:
            element.click()
        except Exception:
            try:
                driver.execute_script("arguments[0].click();", element)
            except Exception:
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
        #print(f"Alert 內容: '{alert_text}'")
        alert.accept()
        return alert_text
    except (TimeoutException, NoAlertPresentException):
        print("沒有找到 alert")
        return None
def search(course_id):
    course_id_input = wait.until(EC.presence_of_element_located((By.ID, "course_id")))
    search_button = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "button.btn.btn-primary")
    ))
            
    course_id_input.clear()
    course_id_input.send_keys(course_id)
    click_element_safely(search_button)

    # 檢查是否有該課程的存在
    try:
        # 嘗試找到課程的行
        course_row = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//tr[contains(., '{course_id}')]")
        ))
        return True  # 找到課程
    except TimeoutException:
        # 若沒找到該課程
        print(f"無課程代碼 {course_id}")
        if course_id in course_ids:
            course_ids.remove(course_id)  # 移除不存在的課程代碼
        return False  # 沒有找到課程

def click_add_course_button(course_id):
    try:
        wait = WebDriverWait(driver, 10)
        # 找到課程所在的行
        course_row = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//tr[contains(., '{course_id}')]")
        ))

        # 檢查是否已經有「退選」按鈕
        try:
            withdraw_button = course_row.find_element(By.XPATH, ".//button[text()='退選']")
            #print(f"課程 {course_id} 已加選過，跳過此課程")
            return False
        except NoSuchElementException:
            pass

        # 尋找並點擊「加選」按鈕
        add_button = course_row.find_element(By.XPATH, ".//button[text()='加選']")
        driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
        time.sleep(1)

        click_element_safely(add_button)
        
        # 等待可能出現的錯誤訊息
        time.sleep(1)
        return True

    except Exception as e:
        #print(f"無法加選課程 {course_id}：{e}")
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

    time.sleep(1)  # 等待登入完成

    # 點擊查詢與選課頁籤
    search_choose = wait.until(EC.presence_of_element_located((By.ID, "nav-profile-2")))
    search_choose.click()

    # 持續執行直到所有課程都選到
    while sorted(successfully_enrolled_courses) != sorted(course_ids):
        for course_id in course_ids:
            if course_id in successfully_enrolled_courses:
                continue

            # 搜尋課程
            if not search(course_id):
                continue
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

                        # 嘗試加選課程
                        while click_add_course_button(course_id):
                            if check_enrollment_failure(driver):
                                print(f"課程 {course_id} 加選失敗:超過學分限制")
                                time.sleep(1)  # 等待錯誤訊息消失
                                if unenrollment(course_id):
                                    search(course_id)
                                else:
                                    break
                                
                            else:
                                if course_id not in successfully_enrolled_courses:
                                    successfully_enrolled_courses.append(course_id)
                                print(f"課程 {course_id} 已成功加選")
                                break
                        else:
                            if course_id not in successfully_enrolled_courses:
                                successfully_enrolled_courses.append(course_id)
                            print(f"課程 {course_id} 已加選過了")
                    else:
                        print(f"課程 {course_id} 加選失敗:名額不足")

                else:
                    print(f"無法獲取課程 {course_id} 的餘額信息")

            except NoSuchElementException:
                if course_id not in successfully_enrolled_courses:
                    successfully_enrolled_courses.append(course_id)
                print(f"課程 {course_id} 已加選過了")

            print(f'目前已成功加選的課程: {successfully_enrolled_courses}')
            time.sleep(1)  # 等待下一次搜尋

finally:
    print(f'已成功加選的課程: {successfully_enrolled_courses}')
    print('搶課系統已完成所有課程之加選')
    # 關閉瀏覽器
    driver.quit()