from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException, NoAlertPresentException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import tkinter as tk
from tkinter import messagebox
import time

class CoursePriorityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("搶課優先順序設定")
        
        # 初始化課程代碼列表
        self.course_data = []
        
        # 設置標題
        self.title_label = tk.Label(root, text="請輸入欲加選的課程代碼", font=("Arial", 14))
        self.title_label.pack(pady=10)
        
        # 設置課程代碼輸入框
        self.course_entry_label = tk.Label(root, text="請輸入課程代碼（需為4位數字）：")
        self.course_entry_label.pack(pady=5)
        
        self.course_entry = tk.Entry(root, width=30)
        self.course_entry.pack(pady=5)
        
        # 添加課程按鈕
        self.add_button = tk.Button(root, text="添加課程", command=self.add_course)
        self.add_button.pack(pady=10)
        
        # 顯示課程列表
        self.course_listbox_label = tk.Label(root, text="課程列表（可手動調整順序）：")
        self.course_listbox_label.pack(pady=5)
        
        self.course_listbox = tk.Listbox(root, width=40, height=10, selectmode=tk.SINGLE)
        self.course_listbox.pack(pady=10)
        
        # 調整順序按鈕
        self.move_up_button = tk.Button(root, text="向上移動", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT, padx=5)
        
        self.move_down_button = tk.Button(root, text="向下移動", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT, padx=5)
        
        # 儲存課程按鈕
        self.save_button = tk.Button(root, text="儲存課程順序", command=self.save_courses)
        self.save_button.pack(pady=10)
        
        # 完成選課按鈕
        self.complete_button = tk.Button(root, text="選課完成，開始搶課", command=self.show_login_window)
        self.complete_button.pack(pady=10)

    def validate_course_code(self, course_code):
        return len(course_code.strip()) == 4 and course_code.isdigit()
    
    def delete_course(self):
        selected_index = self.course_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            course_code = self.course_data[selected_index]
            confirm = messagebox.askyesno("確認刪除", f"是否確定刪除課程代碼 {course_code}?")
            if confirm:
                # 刪除課程
                self.course_data.pop(selected_index)
                self.course_listbox.delete(selected_index)
                messagebox.showinfo("成功", f"課程代碼 {course_code} 已刪除")
        else:
            messagebox.showwarning("錯誤", "請選擇一個課程代碼進行刪除")
    def add_course(self):
        course_code = self.course_entry.get().strip()
        if not course_code:
            messagebox.showwarning("錯誤", "請輸入課程代碼")
            return
            
        if not self.validate_course_code(course_code):
            messagebox.showwarning("錯誤", "課程代碼格式錯誤，請輸入4位數字")
            return
            
        if course_code in self.course_data:
            messagebox.showwarning("錯誤", f"課程代碼 {course_code} 已經存在")
            return
            
        self.course_data.append(course_code)
        self.course_listbox.insert(tk.END, course_code)
        self.course_entry.delete(0, tk.END)
    
    def move_up(self):
        selected_index = self.course_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index > 0:
                course_code = self.course_data[selected_index]
                self.course_data[selected_index] = self.course_data[selected_index - 1]
                self.course_data[selected_index - 1] = course_code
                
                self.course_listbox.delete(selected_index)
                self.course_listbox.insert(selected_index - 1, course_code)
                self.course_listbox.select_set(selected_index - 1)
    
    def move_down(self):
        selected_index = self.course_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            if selected_index < len(self.course_data) - 1:
                course_code = self.course_data[selected_index]
                self.course_data[selected_index] = self.course_data[selected_index + 1]
                self.course_data[selected_index + 1] = course_code
                
                self.course_listbox.delete(selected_index)
                self.course_listbox.insert(selected_index + 1, course_code)
                self.course_listbox.select_set(selected_index + 1)
    
    def save_courses(self):
        if not self.course_data:
            messagebox.showwarning("錯誤", "課程列表為空，請添加課程後再儲存")
            return
        with open("course_priority.txt", "w") as f:
            for course in self.course_data:
                f.write(course + "\n")
        messagebox.showinfo("儲存成功", "課程順序已儲存!")
    
    def show_login_window(self):
        if not self.course_data:
            messagebox.showwarning("錯誤", "請先添加課程")
            return
            
        login_window = tk.Toplevel(self.root)
        login_window.title("登入選課系統")

        tk.Label(login_window, text="帳號：").pack(pady=5)
        account_entry = tk.Entry(login_window, width=30)
        account_entry.pack(pady=5)
        
        tk.Label(login_window, text="密碼：").pack(pady=5)
        password_entry = tk.Entry(login_window, width=30, show="*")
        password_entry.pack(pady=5)

        login_button = tk.Button(
            login_window, 
            text="登入並搶課", 
            command=lambda: self.start_enrollment(
                account_entry.get(), 
                password_entry.get(), 
                login_window
            )
        )
        login_button.pack(pady=10)

    def start_enrollment(self, user_account, user_password, login_window):
        if not user_account or not user_password:
            messagebox.showwarning("錯誤", "帳號或密碼不可為空！")
            return

        course_ids = self.course_data.copy()
        login_window.destroy()
        
        # 建立自動搶課實例並開始執行
        course_selector = CourseSelector(user_account, user_password, course_ids)
        course_selector.run()

class CourseSelector:
    def __init__(self, user_account, user_password, course_ids):
        self.user_account = user_account
        self.user_password = user_password
        self.course_ids = course_ids
        self.successfully_enrolled_courses = []
        self.driver = None
        self.wait = None

    def click_element_safely(self, element, wait_time=10):
        try:
            wait = WebDriverWait(self.driver, wait_time)
            element = wait.until(EC.element_to_be_clickable(element))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            try:
                element.click()
            except Exception:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                except Exception:
                    try:
                        ActionChains(self.driver).move_to_element(element).click().perform()
                    except Exception as e:
                        print(f"所有點擊方法都失敗: {str(e)}")
                        raise e
        except Exception as e:
            print(f"無法點擊元素: {str(e)}")
            raise e

    def handle_and_get_alert(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            alert = wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            return alert_text
        except (TimeoutException, NoAlertPresentException):
            print("沒有找到 alert")
            return None

    def search(self, course_id):
        course_id_input = self.wait.until(EC.presence_of_element_located((By.ID, "course_id")))
        search_button = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.btn.btn-primary")
        ))
                
        course_id_input.clear()
        course_id_input.send_keys(course_id)
        self.click_element_safely(search_button)

        try:
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//tr[contains(., '{course_id}')]")
            ))
            return True
        except TimeoutException:
            print(f"無課程代碼 {course_id}")
            if course_id in self.course_ids:
                self.course_ids.remove(course_id)
            return False

    def check_enrollment_failure(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.text_to_be_present_in_element(
                    (By.ID, "flash-message-2"),
                    "加選後超過 25 學分"
                )
            )
            error_message_element = self.driver.find_element(By.ID, "flash-message-2")
            message_text = error_message_element.text.strip()
            
            if '加選後超過 25 學分' in message_text:
                time.sleep(2)
                return True
            else:
                print(f"其他錯誤訊息: {message_text}")
                time.sleep(2)
                return False
                
        except TimeoutException:
            return False
        except NoSuchElementException:
            print("未找到錯誤訊息元素")
            return False
        except Exception as e:
            print(f"檢查選課狀態時發生錯誤: {str(e)}")
            return False

    def unenrollment(self, course_id):
        try:
            current_priority = self.course_ids.index(course_id)
            lower_priority_courses = []
            for enrolled_course in self.successfully_enrolled_courses:
                enrolled_priority = self.course_ids.index(enrolled_course)
                if enrolled_priority > current_priority:
                    lower_priority_courses.append((enrolled_course, enrolled_priority))
            
            if not lower_priority_courses:
                print(f"沒有優先權較低的課程可以退選")
                return False
                
            lower_priority_courses.sort(key=lambda x: x[1], reverse=True)
            course_to_withdraw = lower_priority_courses[0][0]
            
            course_id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "course_id"))
            )
            search_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-primary"))
            )
            
            course_id_input.clear()
            course_id_input.send_keys(course_to_withdraw)
            self.click_element_safely(search_button)
            time.sleep(1)
            
            try:
                form = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, 
                        f"//tr[.//td[normalize-space(text())='{course_to_withdraw}']]//form[.//button[contains(text(), '退選')]]"))
                )
                
                self.driver.execute_script("""
                    if(confirm('確定要退選此課程嗎？')) {
                        arguments[0].submit();
                    }
                """, form)
                self.handle_and_get_alert()

                time.sleep(1)

                self.search(course_to_withdraw)
               
                time.sleep(1)
                
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, 
                            f"//tr[.//td[normalize-space(text())='{course_to_withdraw}']]//button[text()='加選']"))
                    )
                    self.successfully_enrolled_courses.remove(course_to_withdraw)
                    print(f"已成功退選課程 {course_to_withdraw}")
                    print(f"目前已選課程: {self.successfully_enrolled_courses}")
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

    def click_add_course_button(self, course_id):
        try:
            course_row = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//tr[contains(., '{course_id}')]")
            ))

            try:
                course_row.find_element(By.XPATH, ".//button[text()='退選']")
                return False
            except NoSuchElementException:
                pass

            add_button = course_row.find_element(By.XPATH, ".//button[text()='加選']")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(1)

            self.click_element_safely(add_button)
            time.sleep(1)
            return True

        except Exception as e:
            return False

    def run(self):
        try:
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 10)
            
            self.driver.get("http://127.0.0.1:5000/")

            username_input = self.driver.find_element(By.NAME, "id")
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

            username_input.send_keys(self.user_account)
            password_input.send_keys(self.user_password)
            login_button.click()

            time.sleep(1)

            # 點擊查詢與選課頁籤
            search_choose = self.wait.until(EC.presence_of_element_located((By.ID, "nav-profile-2")))
            search_choose.click()

            # 持續執行直到所有課程都選到
            while sorted(self.successfully_enrolled_courses) != sorted(self.course_ids):
                for course_id in self.course_ids:
                    if course_id in self.successfully_enrolled_courses:
                        continue

                    # 搜尋課程
                    if not self.search(course_id):
                        continue
                    time.sleep(1)

                    try:
                        # 找到並點擊餘額按鈕
                        balance_button = self.wait.until(EC.element_to_be_clickable(
                            (By.XPATH, f"//tr[contains(., '{course_id}')]//button[contains(text(), '餘額')]")
                        ))
                        self.click_element_safely(balance_button)

                        # 處理並獲取餘額 alert 內容
                        alert_text = self.handle_and_get_alert()

                        if alert_text:
                            # 解析餘額資訊
                            available_slots0 = alert_text.split(':')[1].strip().split(' / ')[0]
                            available_slots_int0 = int(available_slots0)
                            available_slots1 = alert_text.split(':')[1].strip().split(' / ')[1]
                            available_slots_int1 = int(available_slots1)

                            if available_slots_int0 < available_slots_int1:
                                time.sleep(1)

                                # 嘗試加選課程
                                while self.click_add_course_button(course_id):
                                    if self.check_enrollment_failure():
                                        print(f"課程 {course_id} 加選失敗:超過學分限制")
                                        time.sleep(1)
                                        if self.unenrollment(course_id):
                                            self.search(course_id)
                                        else:
                                            break
                                    else:
                                        if course_id not in self.successfully_enrolled_courses:
                                            self.successfully_enrolled_courses.append(course_id)
                                        print(f"課程 {course_id} 已成功加選")
                                        break
                                else:
                                    if course_id not in self.successfully_enrolled_courses:
                                        self.successfully_enrolled_courses.append(course_id)
                                    print(f"課程 {course_id} 已加選過了")
                            else:
                                print(f"課程 {course_id} 加選失敗:名額不足")

                        else:
                            print(f"無法獲取課程 {course_id} 的餘額信息")

                    except NoSuchElementException:
                        if course_id not in self.successfully_enrolled_courses:
                            self.successfully_enrolled_courses.append(course_id)
                        print(f"課程 {course_id} 已加選過了")

                    print(f'目前已成功加選的課程: {self.successfully_enrolled_courses}')
                    time.sleep(1)

        except Exception as e:
            messagebox.showerror("錯誤", f"發生錯誤: {str(e)}")
        finally:
            print(f'已成功加選的課程: {self.successfully_enrolled_courses}')
            print('搶課系統已完成所有課程之加選')
            if self.driver:
                self.driver.quit()
            messagebox.showinfo("完成", f"搶課完成！\n成功加選的課程: {', '.join(self.successfully_enrolled_courses)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoursePriorityApp(root)
    root.mainloop()